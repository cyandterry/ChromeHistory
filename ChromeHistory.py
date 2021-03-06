#!/usr/bin/env python

import sqlite3
import urlparse
class AnalyseChrome:
    '''
    User's chrome history log is written by sqllite and saved default in ~/.config/google-chrome/Default/History on ubuntu.
    '''
    def __init__(self,db = '/home/ycao/.config/google-chrome/Default/History'):
        # Init the AnalyseChrome by the chrome history db path.
        self.cn = sqlite3.connect(db)
        self.cu = self.cn.cursor()

    def get_sql_res(self,sql):
        try:
            self.cu.execute(sql)
        except Exception,e:
            print str(e)
            return 0,str(e)
        res = self.cu.fetchall()
        return res,''

    def show_table(self,name = '%'):
        # Show the table in db of History
        sql = "SELECT * FROM sqlite_master WHERE type = 'table' and name like '%s';"%(name,)
        return self.get_sql_res(sql)

    def clear(self,):
        self.cn.close()

    def top_n(self,n = None,orderby = 'host'):
        # Return the top n url or host the user visit frequently.default orderby host
        sql = 'select url,visit_count from urls order by url ;'
        res,errmsg = self.get_sql_res(sql)
        uniq_res = []
        
        '''
        Select all url, visit form urls table sort by url
        Make a new list which has uniq url and new count. by myself.
        Then, sort by python's list.sort().
        Finally print top n.
        '''

        if res:
            urlhost = ''
            for item in res:
                if orderby == 'host':
                    now_urlhost = urlparse.urlparse(item[0]).netloc
                elif orderby == 'url':
                    now_urlhost = item[0]
                else:
                    return None,'error argv in top_n'
                if now_urlhost == '' or now_urlhost == None:
                    continue
                if urlhost != now_urlhost:
                    urlhost,count = now_urlhost,item[1]
                    uniq_res.append([urlhost,count])

                else:
                    uniq_res[-1][-1] = uniq_res[-1][-1] + item[1]
                    continue
        else:
            return None,errmsg
        uniq_res.sort(key = lambda x:x[1],reverse = True)
        return [i for i in uniq_res[0:n]],''

if __name__ == '__main__':
    ac = AnalyseChrome()

    tb,errormsg = ac.show_table('urls')
    if tb:
        for i in  tb:
            print i

    res,errormsg = ac.top_n(20,'host')
    no = 1
    if res:
        for i in res:
            print no,i
            no += 1
    else :
        print errormsg
    ac.clear()
