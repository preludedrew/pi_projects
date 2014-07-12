import web

def readfile(filename):
    global cur_info
    handle = open(filename, 'r')
    cur_info = handle.read()
    handle.close()
    return cur_info

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        return readfile('score.cur')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
