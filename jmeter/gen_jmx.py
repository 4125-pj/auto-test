"""Generate JMeter JMX test plan for login API"""
import xml.etree.ElementTree as ET
from xml.dom import minidom

plan = ET.Element('jmeterTestPlan', attrib={'version': '1.2', 'properties': '5.0', 'jmeter': '5.6.3'})
ht_root = ET.SubElement(plan, 'hashTree')

# TestPlan
tp = ET.SubElement(ht_root, 'TestPlan', {'guiclass': 'TestPlanGui', 'testclass': 'TestPlan', 'testname': '登录接口压测', 'enabled': 'true'})
udv = ET.SubElement(tp, 'elementProp', {'name': 'TestPlan.user_defined_variables', 'elementType': 'Arguments', 'guiclass': 'ArgumentsPanel', 'testclass': 'Arguments', 'testname': '用户变量', 'enabled': 'true'})
ET.SubElement(udv, 'collectionProp', {'name': 'Arguments.arguments'})
ht1 = ET.SubElement(ht_root, 'hashTree')

# CSV
csv = ET.SubElement(ht1, 'CSVDataSet', {'guiclass': 'TestBeanGUI', 'testclass': 'CSVDataSet', 'testname': '读取用户列表', 'enabled': 'true'})
ET.SubElement(csv, 'stringProp', {'name': 'delimiter'}).text = ','
ET.SubElement(csv, 'stringProp', {'name': 'fileEncoding'}).text = 'UTF-8'
ET.SubElement(csv, 'stringProp', {'name': 'filename'}).text = 'plans/users.csv'
ET.SubElement(csv, 'boolProp', {'name': 'ignoreFirstLine'}).text = 'true'
ET.SubElement(csv, 'stringProp', {'name': 'variableNames'}).text = 'username'
ET.SubElement(csv, 'boolProp', {'name': 'recycle'}).text = 'false'
ET.SubElement(csv, 'stringProp', {'name': 'shareMode'}).text = 'shareMode.all'
ht1.append(ET.SubElement(ET.Element('hashTree'), 'dummy'))

# ThreadGroup
tg = ET.SubElement(ht1, 'ThreadGroup', {'guiclass': 'ThreadGroupGui', 'testclass': 'ThreadGroup', 'testname': '登录并发测试', 'enabled': 'true'})
ET.SubElement(tg, 'stringProp', {'name': 'ThreadGroup.on_sample_error'}).text = 'continue'
lc = ET.SubElement(tg, 'elementProp', {'name': 'ThreadGroup.main_controller', 'elementType': 'LoopController', 'guiclass': 'LoopControlPanel', 'testclass': 'LoopController', 'enabled': 'true'})
ET.SubElement(lc, 'boolProp', {'name': 'LoopController.continue_forever'}).text = 'false'
ET.SubElement(lc, 'stringProp', {'name': 'LoopController.loops'}).text = '1'
ET.SubElement(tg, 'stringProp', {'name': 'ThreadGroup.num_threads'}).text = '12'
ET.SubElement(tg, 'stringProp', {'name': 'ThreadGroup.ramp_time'}).text = '12'
ht_tg = ET.SubElement(ht1, 'hashTree')

# Headers
hm = ET.SubElement(ht_tg, 'HeaderManager', {'guiclass': 'HeaderPanel', 'testclass': 'HeaderManager', 'testname': '请求头', 'enabled': 'true'})
col = ET.SubElement(hm, 'collectionProp', {'name': 'HeaderManager.headers'})
ep = ET.SubElement(col, 'elementProp', {'name': '', 'elementType': 'Header'})
ET.SubElement(ep, 'stringProp', {'name': 'Header.name'}).text = 'Content-Type'
ET.SubElement(ep, 'stringProp', {'name': 'Header.value'}).text = 'application/json'
ht_tg.append(ET.SubElement(ET.Element('hashTree'), 'dummy'))

# HTTP Request
req = ET.SubElement(ht_tg, 'HTTPSamplerProxy', {'guiclass': 'HttpTestSampleGui', 'testclass': 'HTTPSamplerProxy', 'testname': '登录', 'enabled': 'true'})
args = ET.SubElement(req, 'elementProp', {'name': 'HTTPsampler.Arguments', 'elementType': 'Arguments'})
ac = ET.SubElement(args, 'collectionProp', {'name': 'Arguments.arguments'})
ap = ET.SubElement(ac, 'elementProp', {'name': '', 'elementType': 'HTTPArgument'})
ET.SubElement(ap, 'boolProp', {'name': 'HTTPArgument.always_encode'}).text = 'false'
ET.SubElement(ap, 'stringProp', {'name': 'Argument.value'}).text = '{"username":"${username}","password":"Lw@123456"}'
ET.SubElement(ap, 'stringProp', {'name': 'Argument.metadata'}).text = '='
ET.SubElement(req, 'stringProp', {'name': 'HTTPSampler.domain'}).text = 'yxj-crm-test-api.hbyxj.com'
ET.SubElement(req, 'stringProp', {'name': 'HTTPSampler.port'}).text = '443'
ET.SubElement(req, 'stringProp', {'name': 'HTTPSampler.protocol'}).text = 'https'
ET.SubElement(req, 'stringProp', {'name': 'HTTPSampler.path'}).text = '/api/auth/login'
ET.SubElement(req, 'stringProp', {'name': 'HTTPSampler.method'}).text = 'POST'
ET.SubElement(req, 'boolProp', {'name': 'HTTPSampler.postBodyRaw'}).text = 'true'
ht_req = ET.SubElement(ht_tg, 'hashTree')


def add_assertion(parent, name, pattern):
    a = ET.SubElement(parent, 'ResponseAssertion', {'guiclass': 'AssertionGui', 'testclass': 'ResponseAssertion', 'testname': name, 'enabled': 'true'})
    cp = ET.SubElement(a, 'collectionProp', {'name': 'Asserion.test_strings'})
    ET.SubElement(cp, 'stringProp', {'name': '49586'}).text = pattern
    ET.SubElement(a, 'stringProp', {'name': 'Assertion.test_field'}).text = 'text'
    ET.SubElement(a, 'boolProp', {'name': 'Assertion.assume_success'}).text = 'false'
    ET.SubElement(a, 'intProp', {'name': 'Assertion.test_type'}).text = '2'
    parent.append(ET.SubElement(ET.Element('hashTree'), 'dummy'))


add_assertion(ht_req, '断言: code=200', '"code":200')
add_assertion(ht_req, '断言: expiresIn不为空', '"expiresIn":72000000')
add_assertion(ht_req, '断言: accessToken不为空', '"accessToken":"eyJ')

# Report listeners
ET.SubElement(ht1, 'ResultCollector', {'guiclass': 'SummaryReport', 'testclass': 'ResultCollector', 'testname': '汇总报告', 'enabled': 'true'})
ht1.append(ET.SubElement(ET.Element('hashTree'), 'dummy'))
ET.SubElement(ht1, 'ResultCollector', {'guiclass': 'StatGraphVisualizer', 'testclass': 'ResultCollector', 'testname': '聚合报告', 'enabled': 'true'})
ht1.append(ET.SubElement(ET.Element('hashTree'), 'dummy'))

# Write
xml_str = ET.tostring(plan, encoding='unicode')
dom = minidom.parseString(xml_str)
pretty = dom.toprettyxml(indent='  ')
with open('plans/login_test.jmx', 'w', encoding='utf-8') as f:
    f.write(pretty)
print('OK: login_test.jmx generated')
