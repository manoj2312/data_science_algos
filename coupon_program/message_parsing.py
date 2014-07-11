def load_into_file(path):
        File=open(path,'r')
        lines=File.readlines()
        exclusion_list_strings=['SBIINB', 'CANBNK', 'iPaytm', 'AIRMTA', 'IRCTCi', 'Sulekh', 'AIROAM', 'SPCJET','FACEBK', 'eBayIN', 'eBayin','FRTRAK','FSTRCK','SPICEJ']
        exclusion=[]
        coupon_line_indices =[]
        for index,line in enumerate(lines):
                for word in exclusion_list_strings:
                    if word in line:
                        exclusion.append(line)
                        coupon_line_indices.append(index)
        File.close()
        coupon_lines = [message for index,message in enumerate(lines) if index not in coupon_line_indices ]
        return coupon_lines, exclusion
    
path = '/home/manu/Documents/Coupons/sms.txt'
coupons, ads = load_into_file(path)
ads_path='/home/manu/Documents/Coupons/ads.txt'
File=open(ads_path,'w')
for ad_line in ads:
    File.write(str(ad_line))
File.close()
coupons_path='/home/manu/Documents/Coupons/coupons.txt'
File=open(coupons_path,'w')
for coupon_line in coupons:
    File.write(str(coupon_line))
File.close()