import argparse
import configparser
import os
from pyChatGPT import ChatGPT
import subprocess


verdict ={
  
    # compiler_error
    "1":"可以告訴我為什麼以下程式碼會編譯錯誤嘛?,語言是",
    # runtime_error
    "2":"可以告訴我為什麼以下程式碼在上述的問題中會出現runtime error嘛?,語言是",
    # time_limit
    "3":"可以告訴我下列程式碼在上述的問題中可能出現time limit的原因嘛?，語言是",
    # wrong_answer
    "4":"可以告訴我為什麼以下程式碼無法解決上述的問題嘛?,語言是"
    
}



def read_file(file_path):
  with open(file_path,"r") as f:
      data =f.read()
  return data 


def create_question_toChatGPT(problem,code,lang,judge_result):
  
  
  match judge_result:
    
    case 1:
      
      prompt = verdict[str(judge_result)]+lang+"\n-----------------------\n"+code
    case _:
      prompt = problem+"\n-----------------------\n"+verdict[str(judge_result)]+lang+"\n-----------------------\n"+code
  
  
  return prompt


def start_chatGPT(opt,judge_result):
  
  
  question_title = opt.title
  code_filepath = opt.code
  lang = opt.lang
  # question filepath
  question_description_filepath= os.path.join(opt.question,f"./{question_title}/description.txt")
  
  # get file data
  problem = read_file(question_description_filepath)
  code = read_file(code_filepath)
  
  prompt = create_question_toChatGPT(problem,code,lang,judge_result)
  
  print(prompt)
  # get session token
  config = configparser.ConfigParser()
  config.read('config.ini')
  session_token = config['session_token']['session_token']
  
  # start connect ChatGPT
  api = ChatGPT(session_token)
  
  rst_message = api.send_message(prompt)["message"]
  api.driver.close()
  print("\n\nreturn message")
  print(rst_message)
  
  with open(opt.save,"w") as f:
    f.write(rst_message)

  

def main(opt):
  
  ret= subprocess.run(f"python3 ./judge.py {opt.title} {opt.code}".split(),capture_output=True)
  judge_result = ret.returncode
  
  if judge_result :
    start_chatGPT(opt,judge_result)

def parse_opt(known):
  
  ROOT = os.getcwd()
  parser =argparse.ArgumentParser()
  parser.add_argument("--question",type=str)
  parser.add_argument("--judge",type=str)
  parser.add_argument("--title",type=str,required=True, help = "question title")
  parser.add_argument("--code",type=str,required=True ,help = "the path of code file ")
  parser.add_argument("--lang",type=str,required=True,help = "you use programming language")
  parser.add_argument("--save",type=str,default="./chatgpt_rst_msg.txt",help = "the path that save the charGPT return message ")
  
  
  return parser.parse_known_args()[0] if known else parser.parse_args()

def run(**kwargs):
  opt=parse_opt(True)
  for k , v in kwargs.items():
      setattr(opt,k,v)
  main(opt)
  return opt
    
if __name__ == "__main__":
  opt = parse_opt(True)
  main(opt)


# python3 ./judge.py BuildingRoads /home/yi-cheng/Desktop/ChatGPT/question/BuildingRoads/solution.cpp

