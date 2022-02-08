from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

fileName = os.path.basename("./filetransfer.txt")
fileContent = open("filetransfer.txt", "r").read()

sentMail = (fileName, fileContent)

if rank == 0:
  comm.send(sentMail, dest=1)
  print("From rank", str(rank), "we sent: ", sentMail)
  
if rank == 1:
  receivedMail = comm.recv(source=0)
  print("From rank", str(rank), "we received: ", receivedMail)
  f = open("./mailbox/" + fileName, "w")
  f.write(receivedMail[1])
  f.close()
  print("Check mail in mailbox!")
