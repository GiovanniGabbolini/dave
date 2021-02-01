// populate db
db = db.getSiblingDB('pilot');
print(db.getCollectionNames());
if (db.getCollectionNames().length == 0) {
	answers = db.answers;
	answers.insertOne({ 'init': 'init' });
	comments = db.comments;
	comments.insertOne({ 'init': 'init' });
}
// enable access control
db = db.getSiblingDB('admin');
db.createUser(
	{
		user: "giovanni",
		pwd: passwordPrompt(), // or cleartext password
		roles: [{ role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase"]
	}
)
// shutdown
db.adminCommand({ shutdown: 1 })