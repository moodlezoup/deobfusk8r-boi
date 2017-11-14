import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;

import org.xmlpull.v1.XmlPullParserException;

import soot.PackManager;
import soot.Scene;
import soot.SootMethod;
import soot.jimple.infoflow.android.SetupApplication;
import soot.jimple.toolkits.callgraph.CallGraph;
import soot.jimple.toolkits.callgraph.Edge;
import soot.options.Options;

//dump the call graph from FlowDroid
public class CFG {
	public CFG(){}

  static private class IDMap {
    int freshID = 0;
    Map<String, Integer> map = new HashMap<String, Integer>();
	  public IDMap(){}

    public int getId(String signature) {
        if(map.containsKey(signature)){
          return map.get(signature);
        }else{
          int id = freshID;
          freshID += 1;
          map.put(signature, id);
          return id;
        }
    }

    public Set<Map.Entry<String, Integer>>  entrySet() {
      return map.entrySet();
    }

  }

  private static void clearFile(File f) {
			if(f.exists()){
				f.delete();
			}
  }
	
	//output the call graph to JSON formate
	private static void outputCallGraph(CallGraph cg, String apkTitle) throws IOException {
		Path curDir = Paths.get(System.getProperty("user.dir"));

		Path edgeOutputPath = Paths.get(curDir.toString(), apkTitle + ".edges");
		File edgeOut = edgeOutputPath.toFile();
    clearFile(edgeOut);
		FileWriter edgeOutFW = new FileWriter(edgeOut);

		Path keyOutputPath = Paths.get(curDir.toString(), apkTitle + ".key");
		File keyOut = keyOutputPath.toFile();
		FileWriter keyOutFW = new FileWriter(keyOut);

		Iterator<Edge> itr = cg.iterator();

    IDMap map = new IDMap();

		while(itr.hasNext()){
			Edge e = itr.next();
      int srcId = map.getId(e.getSrc().toString());
      int dstId = map.getId(e.getTgt().toString());
      edgeOutFW.write(String.format("%d %d\n", srcId, dstId));
		}
    for (Map.Entry<String, Integer> entry : map.entrySet())
    {
      keyOutFW.write(String.format("%d %s\n", entry.getValue(), entry.getKey()));
    }
    keyOutFW.flush();
    keyOutFW.close();
    edgeOutFW.flush();
    edgeOutFW.close();
		System.out.println("Written to files: " + keyOut.getName() + " and " + edgeOut.getName());
	}
	
	private static void printUsage(){
		System.out.println("Usage: apk-file, android-jar-directory");		
	}
	
	public static void main(String[] args){
		if (args.length < 2){
			printUsage();
			return;
		}
		
		String apkPath = args[0];
		String androidJarPath = args[1];

    File apkFile = new File(apkPath);
    String apkFileName = apkFile.getName();
    int dotIndex = apkFileName.lastIndexOf(".");
    String extension = apkFileName.substring(dotIndex);
    if (!extension.equals(".apk") || !apkFile.exists()){
      System.out.println("apk-file "+ apkFile.getName() + " does not exist");
      return;
    }

		SetupApplication app = new SetupApplication(androidJarPath, apkPath);
    app.setCallbackFile("AndroidCallbacks.txt");

    app.constructCallgraph();

    CallGraph cg = Scene.v().getCallGraph();

		System.out.println("Call graph size: "+ cg.size());		
    try {
      outputCallGraph(cg, apkFileName.substring(0, dotIndex));
    } catch (IOException e) {
      e.printStackTrace();
    }
	}
}
