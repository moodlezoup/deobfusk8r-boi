import sbt._

object ArgusVersions {
  val scalaVersion = "2.12.2"
  val sbtVersion = "0.13.13"
}

object Dependencies {
  import ArgusVersions._

  val sbtLaunch: ModuleID = "org.scala-sbt" % "sbt-launch" % sbtVersion

  val commons_cli: ModuleID = "commons-cli" % "commons-cli" % "1.3.1"

  val amandroid_core: ModuleID = "com.github.arguslab" %% "amandroid" % "3.1.2"
}

object DependencyGroups {
  import Dependencies._

  val extractor = Seq(
    commons_cli,
    amandroid_core
  )
}
