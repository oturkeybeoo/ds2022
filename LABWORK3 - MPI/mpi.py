from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
file = open("filetotransfer.txt", "r").read()
if rank == 0:
  comm.send(file, dest=1)
  print("From rank", str(rank), "we sent: ", file)
if rank == 1:
  data = comm.recv(source=0)
  print("From rank", str(rank), "we received: ", data)
