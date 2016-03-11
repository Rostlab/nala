import java.io.File
import scala.io.Source
import scala.collection.mutable

val MAP = Source.fromFile(new File("map_docs_to_itrs.txt")).getLines.foldLeft(Map[String, String]()) { (map, line) =>
  val Array(itr, docid) = line.split(" ")
  assert(!map.contains(docid))
  map + ((docid, itr))
}

var annotator: String = null
val assignment = "(\\w+) [0-9]+ \\[(.*)\\]".r
val doc = "\\s+(a.*)".r
val groupItrs = mutable.Map[String, Set[String]]()

Source.fromFile(new File("README.md")).getLines.foreach { line =>
  line match {
    case assignment(name, itrs) => {
      if (name != "test" && name != "IAA") {
        annotator = name
      }
      else {
        groupItrs(name) = itrs.split("\\s*,\\s*").toSet
        println(groupItrs)
      }
    }
    case _ => {
      line match {
        case doc(docid) if annotator != null => {
          val origFile = new File(s"""${annotator}/${docid}.ann.json""")
          val exists = origFile.exists
          assert(exists, s"""\t${origFile.getName} -> ${exists}""")

          val itr = MAP(docid)
          val isIAA = groupItrs("IAA").contains(itr)
          val destFolder = {
            if (isIAA) {
              new File(s"""../iteration_${itr}/reviewed/${annotator}/""")
            }
            else {
              new File(s"""../iteration_${itr}/reviewed/""")
            }
          }
          //File.mkdirs(destFolder)
          val destFile = new File(destFolder, s"""${docid}.ann.json""")

          println(s"""${origFile.getAbsolutePath} --> ${destFile.getAbsolutePath}""")
          //origFile.renameTo(destFile)
        }
        case _ =>
      }
    }
  }
}
