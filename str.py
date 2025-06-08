from pyrogram import Client

api_id = int(input("API ID: "))
api_hash = input("API Hash: ")

app = Client(name="gen", api_id=api_id, api_hash=api_hash)

app.start()
print("\n✅ String session generated successfully:")
print(app.export_session_string())
app.stop()
