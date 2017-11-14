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

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

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
	
	//output the call graph to JSON formate
	private static String dumpCallGraph(CallGraph cg){
		Iterator<Edge> itr = cg.iterator();
		Map<String, Set<String>> map = new HashMap<String, Set<String>>();

		while(itr.hasNext()){
			Edge e = itr.next();
			String srcSig = e.getSrc().toString();
			String destSig = e.getTgt().toString();
			Set<String> neighborSet;
			if(map.containsKey(srcSig)){
				neighborSet = map.get(srcSig);
			}else{
				neighborSet = new HashSet<String>();
			}
			neighborSet.add(destSig);
			map.put(srcSig, neighborSet );
			
		}
		Gson gson = new GsonBuilder().disableHtmlEscaping().create();
		String json = gson.toJson(map);
		return json;
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

		System.out.println("Call graph size: "+ Scene.v().getCallGraph().size());		
		String res = dumpCallGraph(Scene.v().getCallGraph());

		Path curDir = Paths.get(System.getProperty("user.dir"));
		//where the JSON file is outputed 
    String apkTitle = apkFileName.substring(0, dotIndex);
		Path outputPath = Paths.get(curDir.toString(), apkTitle + ".cfg");
		
		File out = outputPath.toFile();
		try {
			if(out.exists()){
				out.delete();
			}
			FileWriter fw = new FileWriter(out);
			fw.write(res);
			fw.flush();
			fw.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		System.out.println("Written to file: "+outputPath);
	}
}
