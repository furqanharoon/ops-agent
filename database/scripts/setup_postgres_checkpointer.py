with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
  print(type(checkpointer))
  checkpointer.setup()
  print("Setup completed")

