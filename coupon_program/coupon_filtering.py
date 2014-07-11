def load_into_file(path):
        File=open(path,'r')
        lines=File.readlines()
        header = []
        date=[]
        company_id=[]
        message = []
        for line in lines:
                header = line.split(':')[0]
                date.append(header.split(' - ')[0])
                company_id.append(header.split(' - ')[1:])
                message.append(line.split(':')[1:])
        File.close()
        return company_id, date, message
    
path = '/home/manu/Documents/Coupons/coupons.txt'
companies, dates, messages = load_into_file(path)
filters=[]
for msg in messages:
    for word in msg[0].split(' '):
        filters.append(word)
print filters