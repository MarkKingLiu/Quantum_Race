from ezQpy import * 

account = Account(login_key='8de0e9fa225c02094160839ea682e97b', machine_name='ClosedBetaQC')
qcis_circuit = '''
H Q7
X Q1
H Q1
CZ Q7 Q1
H Q1
M Q7
M Q1
'''
isq_code = '''
qbit q[2];
H<q[0]>;
CNOT<q[0], q[1]>;
M<q[0,1]>;
'''

#M<q[0,3]>;
from isq import LocalDevice
ld = LocalDevice()
ir = ld.compile_to_ir(isq_code, target = "qcis")
print(ir)
isq_qcis=ir
isq_qcis = account.qcis_mapping_isq(isq_qcis)
query_id_isQ = account.submit_job(circuit=isq_qcis,version="Bell_state_isQ")
#query_id = account.submit_job(qcis_circuit)
if query_id_isQ:
    result=account.query_experiment(query_id_isQ, max_wait_time=360000)
    #result目前为线路返回的数据，各式在内测期间有可能调整，如果已开发程序后期运行出错，可以考虑符合一下这里的格式，并根据具体情况调整。
    #现阶段2023年4月14日，首批内测时，所约定的格式如下：
    #返回值为字典形式，
    #key-"result"为线路执行的原始数据，共计1+num_shots个数据，第一个数据为测量的比特编号和顺序，其余为每shot对应的结果。
    #key-"probability"为线路测量结果的概率统计，经过实时的读取修正后的统计结果。已知number of shots较少时，读取修正后有可能得到部分概率为负值。
    #"probability"中概率为0的结果不回传。
    #当测量比特大于10个时，"probability"为空，请用户自行根据原始数据，配合当时量子计算机的读出保真度自行做修正。相关修正函数在高阶教程中有示例。用户也可以自己完善修正函数。
    #最大等待时间单位为秒，不传递时默认为30秒。因量子程序的执行会有排队的情况，而量子计算机本身有自动校准的时间，如果想跑全自动的程序，等待时间最好大于两者。
    
    #以下是实验结果的显示、使用与保存。
    #打印，显示结果
    print(result)
    #实验结果为原始数据，数据较长。这里不打印，如有兴趣观察实验结果结构，可以选择打印。
    #每次shot的比特测量结果数据，便于灵活使用，如果需要统计结果，可见高阶教程。
    #选出、处理部分结果示例
    value = result
    #print(value)
    #实验结果为原始数据，数据较长。这里不打印，如有兴趣观察实验结果结构，可以选择打印。
    #保存结果
    f = open("./results.txt",'w')
    f.write(str(value))
    f.close()
    print("实验结果已存盘。")
else :
    #实验未运行成功，需要后继重新提交等处理
    print("实验运行异常，需要重新提交或运行")
res=account.download_config()
#机器完整参数将以json文件形式存储在当前目录。
print(res)