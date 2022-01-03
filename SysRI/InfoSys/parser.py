import string

def Newsgroup(file):
  subject = ''
  text = ''
  ss = 0
  line = 1
  while line:
    line = file.readline()
    if s and line.split()[0] == 'Subject:':
            s = 0
            subject = ' '.join(line.split()[1:])
            continue
    text += line
  
  return {subject, text}

  

