import sbt.Keys._
import sbtassembly.AssemblyPlugin.autoImport._
import sbtbuildinfo.BuildInfoPlugin.autoImport._

val extractorSettings = Defaults.coreDefaultSettings ++ Seq(
  libraryDependencies += "org.scala-lang" % "scala-compiler" % ArgusVersions.scalaVersion,
  scalacOptions ++= Seq("-unchecked", "-deprecation", "-feature")
)
val buildInfoSettings = Seq(
  // build info
  buildInfoKeys := Seq[BuildInfoKey](name, version, scalaVersion, sbtVersion),
  buildInfoPackage := "com.deobfusk8rboi"
)
val assemblySettings = Seq(
  assemblyJarName in assembly := s"${name.value}.jar",
  mainClass in assembly := Some("com.deobfusk8rboi.argussafcfg.Main")
)

val pname = "Argus-SAF-CFG-Extractor"
lazy val argus_saf_cfg_extractor: Project =
  Project(pname, file("."))
    .settings(
      name := pname,
      organization := "com.deobfusk8rboi",
      scalaVersion := ArgusVersions.scalaVersion
    )
    .enablePlugins(BuildInfoPlugin)
    .settings(libraryDependencies ++= DependencyGroups.extractor)
    .settings(extractorSettings)
    .settings(buildInfoSettings)
    .settings(assemblySettings)
    .settings(
      artifact in (Compile, assembly) ~= { art =>
        art.copy(`classifier` = Some("assembly"))
      },
      addArtifact(artifact in (Compile, assembly), assembly),
      publishArtifact in (Compile, packageBin) := false,
      publishArtifact in (Compile, packageDoc) := false,
      publishArtifact in (Compile, packageSrc) := false
    )
