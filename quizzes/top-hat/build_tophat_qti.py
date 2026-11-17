#!/usr/bin/env python3
"""Build and validate a Top Hat class quiz as a Canvas-export-shaped QTI 1.2 zip.

The format rules live in READING-CHECK-QUIZ-QTI-WORKFLOW.md. This file is identical
in both textbook repositories; change it in both, in matching pull requests.

Usage: python3 quizzes/top-hat/build_tophat_qti.py quizzes/top-hat/<course>/session-NN.json <output folder>
"""
import hashlib, json, sys, zipfile, io
from html import escape
from xml.etree import ElementTree as ET

SLOT_ORDER = ["vocab"] * 3 + ["reading"] * 2 + ["anchor"] + ["retrieval"] * 3 + ["prep"]
PREP_STEM = "Did you fully prepare for class today?"


def gid(*parts):
    return "g" + hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()


def html_text(s):
    return escape(f"<div><p>{escape(s, quote=False)}</p></div>", quote=False)


def item_xml(quiz, i, it):
    iid = gid(quiz["slug"], "item", i)
    labels = [gid(quiz["slug"], i, "choice", k) for k in range(len(it["choices"]))]
    resp = "\n".join(
        f'''            <response_label ident="{labels[k]}">
              <material>
                <mattext texttype="text/plain">{escape(c, quote=False)}</mattext>
              </material>
            </response_label>''' for k, c in enumerate(it["choices"]))
    return f'''      <item ident="{iid}" title="Question {i + 1}" maxattempts="1">
        <itemmetadata>
          <qtimetadata>
            <qtimetadatafield><fieldlabel>question_type</fieldlabel><fieldentry>multiple_choice_question</fieldentry></qtimetadatafield>
            <qtimetadatafield><fieldlabel>points_possible</fieldlabel><fieldentry>1.0</fieldentry></qtimetadatafield>
            <qtimetadatafield><fieldlabel>original_answer_ids</fieldlabel><fieldentry>{",".join(labels)}</fieldentry></qtimetadatafield>
            <qtimetadatafield><fieldlabel>assessment_question_identifierref</fieldlabel><fieldentry>{gid(quiz["slug"], "aq", i)}</fieldentry></qtimetadatafield>
          </qtimetadata>
        </itemmetadata>
        <presentation>
          <material>
            <mattext texttype="text/html">{html_text(it["stem"])}</mattext>
          </material>
          <response_lid ident="response1" rcardinality="Single">
            <render_choice shuffle="No">
{resp}
            </render_choice>
          </response_lid>
        </presentation>
        <resprocessing>
          <outcomes>
            <decvar maxvalue="100" minvalue="0" varname="SCORE" vartype="Decimal"/>
          </outcomes>
          <respcondition continue="No">
            <conditionvar>
              <varequal respident="response1">{labels[it["answer"]]}</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
        </resprocessing>
      </item>'''


def build(quiz):
    aid = gid(quiz["slug"], "assessment")
    meta_id = gid(quiz["slug"], "meta")
    n = len(quiz["items"])
    title = escape(quiz["title"], quote=False)
    items = "\n".join(item_xml(quiz, i, it) for i, it in enumerate(quiz["items"]))
    qti = f'''<?xml version="1.0" encoding="UTF-8"?>
<questestinterop xmlns="http://www.imsglobal.org/xsd/ims_qtiasiv1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/ims_qtiasiv1p2 http://www.imsglobal.org/xsd/ims_qtiasiv1p2p1.xsd">
  <assessment ident="{aid}" title="{title}">
    <qtimetadata>
      <qtimetadatafield><fieldlabel>cc_maxattempts</fieldlabel><fieldentry>1</fieldentry></qtimetadatafield>
    </qtimetadata>
    <section ident="root_section">
     <section ident="{gid(quiz["slug"], "section")}" title="{title}">
{items}
     </section>
    </section>
  </assessment>
</questestinterop>
'''
    meta = f'''<?xml version="1.0" encoding="UTF-8"?>
<quiz identifier="{aid}" xmlns="http://canvas.instructure.com/xsd/cccv1p0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://canvas.instructure.com/xsd/cccv1p0 https://canvas.instructure.com/xsd/cccv1p0.xsd">
  <title>{title}</title>
  <description></description>
  <shuffle_answers>false</shuffle_answers>
  <scoring_policy>keep_highest</scoring_policy>
  <quiz_type>assignment</quiz_type>
  <points_possible>{n}.0</points_possible>
  <allowed_attempts>1</allowed_attempts>
  <one_question_at_a_time>false</one_question_at_a_time>
  <cant_go_back>false</cant_go_back>
  <available>false</available>
  <assignment_group_identifierref></assignment_group_identifierref>
</quiz>
'''
    manifest = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{gid(quiz["slug"], "manifest")}" xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1" xmlns:lom="http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource" xmlns:imsmd="http://www.imsglobal.org/xsd/imsmd_v1p2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1 http://www.imsglobal.org/xsd/imscp_v1p1.xsd http://ltsc.ieee.org/xsd/imsccv1p1/LOM/resource http://www.imsglobal.org/profile/cc/ccv1p1/LOM/ccv1p1_lomresource_v1p0.xsd http://www.imsglobal.org/xsd/imsmd_v1p2 http://www.imsglobal.org/xsd/imsmd_v1p2p2.xsd">
  <metadata>
    <schema>IMS Content</schema>
    <schemaversion>1.1.3</schemaversion>
  </metadata>
  <organizations/>
  <resources>
    <resource identifier="{aid}" type="imsqti_xmlv1p2">
      <file href="{aid}/{aid}.xml"/>
      <dependency identifierref="{meta_id}"/>
    </resource>
    <resource identifier="{meta_id}" type="associatedcontent/imscc_xmlv1p1/learning-application-resource" href="{aid}/assessment_meta.xml">
      <file href="{aid}/assessment_meta.xml"/>
      <file href="{aid}/assessment_qti.xml"/>
      <file href="non_cc_assessments/{aid}.xml.qti"/>
    </resource>
  </resources>
</manifest>
'''
    files = {
        "imsmanifest.xml": manifest,
        f"{aid}/{aid}.xml": qti,
        f"{aid}/assessment_qti.xml": qti,
        f"{aid}/assessment_meta.xml": meta,
        f"non_cc_assessments/{aid}.xml.qti": qti,
        "course_settings/canvas_export.txt": "common_cartridge\n",
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, body in files.items():
            z.writestr(name, body)
    return buf.getvalue()


def check_content(quiz):
    items = quiz["items"]
    assert len(items) == 10, "a class quiz has ten questions"
    assert [it["slot"] for it in items] == SLOT_ORDER, "slots out of order"
    assert items[-1]["stem"] == PREP_STEM and items[-1]["choices"] == ["Yes", "No"]
    for i, it in enumerate(items[:-1], 1):
        c = it["choices"]
        allowed = (2, 3, 4) if it["slot"] == "retrieval" and it.get("reused_practice_item") else (4,)
        assert len(c) in allowed and len(set(c)) == len(c), f"Q{i}: needs {allowed} distinct choices"
        assert 0 <= it["answer"] < len(c)
        lens = [len(x) for x in c]
        if lens[it["answer"]] == max(lens) and lens.count(max(lens)) == 1 and max(lens) > 1.25 * sorted(lens)[-2]:
            raise AssertionError(f"Q{i}: correct answer is clearly the longest")
    pos = [it["answer"] for it in items[:-1]]
    counts = {"ABCD"[k]: pos.count(k) for k in range(4)}
    assert max(counts.values()) <= 3, f"answer positions unbalanced: {counts}"
    return counts


def check_zip(data, quiz):
    z = zipfile.ZipFile(io.BytesIO(data))
    assert z.testzip() is None
    names = set(z.namelist())
    ns = {"m": "http://www.imsglobal.org/xsd/imsccv1p1/imscp_v1p1"}
    man = ET.fromstring(z.read("imsmanifest.xml"))
    res = man.findall(".//m:resource", ns)
    assert res[0].get("type") == "imsqti_xmlv1p2"
    assert res[0].find("m:dependency", ns).get("identifierref") == res[1].get("identifier")
    for f in man.findall(".//m:file", ns):
        assert f.get("href") in names, f"manifest path missing: {f.get('href')}"
    qtis = [n for n in names if n.endswith(".xml.qti") or n.endswith("assessment_qti.xml")
            or (n.count("/") == 1 and n.split("/")[0] + ".xml" == n.split("/")[1])]
    blobs = {z.read(n) for n in qtis}
    assert len(qtis) == 3 and len(blobs) == 1, "QTI copies must be identical"
    q = ET.fromstring(blobs.pop())
    qn = "{http://www.imsglobal.org/xsd/ims_qtiasiv1p2}"
    items = q.findall(f".//{qn}item")
    assert len(items) == len(quiz["items"])
    assert q.find(f".//{qn}section").get("ident") == "root_section"
    for el, it in zip(items, quiz["items"]):
        labels = el.findall(f".//{qn}response_label")
        assert len(labels) == len(it["choices"])
        assert el.find(f".//{qn}render_choice").get("shuffle") == "No"
        keys = el.findall(f".//{qn}varequal")
        assert len(keys) == 1
        keyed = [l for l in labels if l.get("ident") == keys[0].text]
        assert keyed and keyed[0].find(f".//{qn}mattext").text == it["choices"][it["answer"]]
        f = {m.find(f"{qn}fieldlabel").text: m.find(f"{qn}fieldentry").text
             for m in el.findall(f".//{qn}qtimetadatafield")}
        assert f["question_type"] == "multiple_choice_question" and f["points_possible"] == "1.0"
    return sorted(names)


if __name__ == "__main__":
    quiz = json.load(open(sys.argv[1], encoding="utf-8"))
    counts = check_content(quiz)
    data = build(quiz)
    names = check_zip(data, quiz)
    out = f"{sys.argv[2]}/{quiz['slug']}_tophat_qti.zip"
    open(out, "wb").write(data)
    print("OK", out)
    print("answer positions (A-D):", counts)
    print("\n".join("  " + n for n in names))
