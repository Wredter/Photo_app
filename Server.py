import web
import os 
import time;

urls = (
    '/', 'Index',
    '/upload', 'Upload',
    '/result', 'Result'
)

lastOutputJson = "none"

class Index:
    def GET(self):
        return "Hello, world!"


class Result:
    def GET(self):
        return "Result"



class Upload:
    def GET(self):
        return """<html><head></head><body>
        <h1>PhotoApp</h1>
        <h2>Upload Your photo here</h2>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        print("HI________________")
        web.debug(x['myfile'].filename) # This is the filename
    # ??    web.debug(x['myfile'].value) # This is the file contents
        print("HI___________WAIT...")

        # filedir = '/Users/stanislawpulawski/data/dockervolumes/minio/photo' # My Laptop
        # filedir = '/home/zombie/data/minio/photo' # Azure VM
        filedir = '/data/minio/photo' # Container
        
        timestamp = str(int(time.time()))
        os.system("cd {} && mkdir {}".format(filedir, timestamp))
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            wholeFilepath = str(filedir +'/'+ timestamp +'/'+ 'inputfile')
            fout = open(filedir +'/'+ timestamp +'/'+ 'inputfile','wb') # creates the file where the uploaded file should be stored
            fout = open(wholeFilepath,'wb') # creates the file where the uploaded file should be stored
            # fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        print(wholeFilepath)    
        lastOutputJson = str('/data/minio/photo/'+timestamp+"/inputfile")    
        print(lastOutputJson)    
        newFilepath = wholeFilepath.replace("inputfile", "outputfile.json")

        print(newFilepath)
        # print(newFilepath.replace("inputfile", "outputfile.json"))
        runFaceRecognitionCommand = str("python /app/Start.py -f {} -o {}".format(wholeFilepath, lastOutputJson))
        os.system(runFaceRecognitionCommand)
        # os.system("python ./Start.py -f newFilepath -o lastOutputJson")
        # os.system("python /app/Wait.py -t 1")
        print("HI___________END...")
        raise web.seeother('/result')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()