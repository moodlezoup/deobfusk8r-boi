package com.deobfusk8rboi.argussafcfg

import org.apache.commons.cli._
import org.argus.jawa.core.util._

import org.argus.jawa.alir.pta.suspark.InterProceduralSuperSpark
import org.argus.amandroid.alir.componentSummary.{ApkYard, ComponentBasedAnalysis}
import org.argus.amandroid.core.decompile.{DecompileLayout, DecompileStrategy, DecompilerSettings}
import org.argus.amandroid.core.{AndroidConstants, ApkGlobal}
import org.argus.jawa.core.DefaultReporter
import org.argus.jawa.core.util.FileUtil
import java.io._
import org.argus.jawa.alir.reachability.SignatureBasedCallGraph
import org.argus.jawa.core.Signature
import scala.collection.mutable.Map
import org.argus.jawa.core.util.{IList, ISet, isetEmpty}
import scala.language.postfixOps
import scala.concurrent.duration._

object Main extends App {
  // create the command line parser
  val parser: CommandLineParser = new DefaultParser()
  var commandLine: CommandLine = _

  try {
    // parse the command line arguments
    commandLine = parser.parse(new Options, args)
    var sourcePath: String = null
    sourcePath = commandLine.getArgList.get(0)
    decompile(sourcePath)
  } catch {
    case exp: Exception =>
      println("Something's wrong:" + exp.getMessage)
      val sw = new StringWriter
      exp.printStackTrace(new PrintWriter(sw))
      println(sw.toString)
      System.exit(0)
  }

  def reaching_facts_strat(apk: ApkGlobal): IMap[Signature, ISet[Signature]] = {
    val apks = isetEmpty + apk
    ComponentBasedAnalysis.prepare(apks)(100 minutes)
    var bigcm : IMap[Signature, ISet[Signature]] = imapEmpty
    apk.getIDFGs foreach {case (t_component, idfg) => {
      println(t_component)
      val icfg = idfg.icfg
      val cg = icfg.getCallGraph
      cg.getCallMap foreach {case (src, dsts) => {
        bigcm = bigcm get src match {
          case None => bigcm + (src -> dsts)
          case Some(old_dsts) => bigcm + (src -> (old_dsts ++ dsts))
        }
      }}
    }}
    bigcm
  }

  def sig_based_strat(apk: ApkGlobal): IMap[Signature, ISet[Signature]] = {
    val component_infos = apk.model.getComponentInfos
    val mappedEntryPoints = component_infos.flatMap(x => apk.getEntryPoints(x))
    val cg = SignatureBasedCallGraph(apk, mappedEntryPoints, None)
    cg.getCallMap
  }

  def decompile(sourcePath: String): Unit = {
    val fileUri = FileUtil.toUri(sourcePath)
    val outputUri = FileUtil.toUri(".argus-pag-output")
    val reporter = new DefaultReporter
    // Yard is the apks manager
    val yard = new ApkYard(reporter)
    val layout = DecompileLayout(outputUri)
    val strategy = DecompileStrategy(layout)
    val settings = DecompilerSettings(debugMode = false, forceDelete = true, strategy, reporter)
    val apk = yard.loadApk(fileUri, settings, collectInfo = true, resolveCallBack = true)
    val edges = new FileWriter(new File("out.edges" ))
    val keys = new FileWriter(new File("out.keys" ))
    dump(reaching_facts_strat(apk), edges, keys)
    keys.flush()
    keys.close()
    edges.flush()
    edges.close()
  }

  class IDMap {
    var freshID: Integer = 0
    val map : Map[Signature, Integer] = Map()

    private def getFreshID(): Integer = {
      val id = freshID
      freshID += 1
      id
    }

    def getId(signature: Signature): Integer =
      map.getOrElseUpdate(signature, getFreshID())
  }

  def dump(callmap: IMap[Signature, ISet[Signature]], edges: FileWriter, keys: FileWriter): Unit = {
    val idmap = new IDMap();
    var x = 0
    callmap.keys.foreach(src => {
      val srcid = idmap.getId(src)
      callmap(src).foreach(dst => {
        val dstid = idmap.getId(dst)
        edges.write(s"$srcid $dstid\n")
        x += 1
      })
    })
    idmap.map.keys.foreach(sig => {
      val id = idmap.map(sig)
      val claname = sig.getClassName
      val rtt = sig.getReturnType.canonicalName
      val paramlist = sig.getParameterTypes
      var l : Array[String] = Array()
      paramlist.foreach(x => l = (l :+ x.canonicalName))
      val params = l.mkString(", ")
      val name = sig.methodName
      keys.write(s"$id <$claname: $rtt $name($params)>\n")
    })
    println(x)
  }
}
