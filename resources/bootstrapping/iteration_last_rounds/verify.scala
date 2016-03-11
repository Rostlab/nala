import java.io.File
import scala.io.Source

val readme = new File("README.md")

var annotator: String = null

val assignment = "(\\w+) [0-9]+ \\[.*".r
val doc = "\\s+(a.*)".r

Source.fromFile(readme).getLines.foreach { line =>
  line match {
    case assignment(name) if name != "IAA" && name != "test" => {
      annotator = name
      println(name)
    }
    case _ => {
      line match {
        case doc(docid) if annotator != null => {
          val exists = new File(s"""${annotator}/${docid}.ann.json""").exists
          println(s"""\t${docid} -> ${exists}""")
          assert(exists)
        }
        case _ =>
      }
    }
  }
}
