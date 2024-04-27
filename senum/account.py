class Account:
    def __init__(self, id,public_key, private_key,google_account,google_password,wallet_password):
        self.id = id
        self.public_key = public_key
        self.private_key = private_key
        self.google_account = google_account
        self.google_password = google_password
        self.wallet_password = wallet_password

import pymysql
def get_all_accounts() -> []:
    # 打开数据库连接
    try:
        db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='web3')
        print('连接成功！')
    except:
        print('something wrong!')

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT * FROM account"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        results_list = []
        for row in results:
            id = row[0]
            public_key = row[1]
            private_key = row[2]
            google_account = row[3]
            google_password = row[4]
            wallet_password = row[5]
            account = Account(id,public_key,private_key,google_account,google_password,wallet_password)
            results_list.append(account)
    except:
        print("Error: unable to fetch data")

    # 关闭数据库连接
    db.close()
    return results_list


print(get_all_accounts())