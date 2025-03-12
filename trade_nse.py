from time import sleep
import zerodha as th
import datetime
from datetime import date,timedelta
import talib as tb
import json
import os
import math
import pandas as pd
#change name,hedge multi, hedge break limit of 50, change in india vix for sensex, change tradehull1, CHANGE NAME IN 2ND TRAE SENBEX

objm=th.Tradehull("api_key","secret_key",'yes')
kite=objm.kite  

#changable variable

def date_ext1(x):
    z=str(date.today())
    y=z+' '+x
    return datetime.datetime.strptime(y,'%Y-%m-%d %H:%M:%S')

#universal variable
#from datetime import datetime
date_string = f"{date.today()}"
date_obj = datetime.datetime.strptime(date_string, '%Y-%m-%d')
day = date_obj.strftime('%A')

#holiday
h1='October 02, 2024' #wednesday
h2='November 01, 2024' #friday
h3='November 15, 2024' #friday
h4='December 25, 2024' #wednesday


if day=='Friday':
    name='NIFTY MID SELECT'
    step=25
    exchange_name='NSE'
    option_exchange='NFO'
    entry_decay=1
    #INTRADAY
    name2='SENSEX'
    step2=100
    exchange_name2='BSE'
    option_exchange2='BFO'
    add_point=6
    
if day=='Monday':
    name='NIFTY FIN SERVICE'
    step=50
    exchange_name='NSE'
    option_exchange='NFO'
    entry_decay=1.5
    #INTRADAY
    name2='NIFTY MID SELECT'
    step2=25
    exchange_name2='NSE'
    option_exchange2='NFO'
    add_point=1.1

if day=='Tuesday':
    name='NIFTY BANK'
    step=100
    exchange_name='NSE'
    option_exchange='NFO'
    entry_decay=2
    #INTRADAY
    name2='NIFTY FIN SERVICE'
    step2=50
    exchange_name2='NSE'
    option_exchange2='NFO'
    add_point=2.2

if day=='Wednesday':
    name='NIFTY 50'
    step=50
    exchange_name='NSE'
    option_exchange='NFO'
    entry_decay=1.5
    #INTRADAY
    name2='NIFTY BANK'
    step2=100
    exchange_name2='NSE'
    option_exchange2='NFO'
    add_point=5

if day=='Thursday':
    name='SENSEX'
    step=100
    exchange_name='BSE'
    option_exchange='BFO'
    entry_decay=3.5
    #INTRADAY
    name2='NIFTY 50'
    step2=50
    exchange_name2='NSE'
    option_exchange2='NFO'
    add_point=2.2


'''name='NIFTY 50'
step=50'''

#variable of variable
ltp_banknifty_at_916am=objm.get_data_for_single_script(exchange_name,name,"ltp")
ltp_banknifty_at_916am=ltp_banknifty_at_916am*0.006
nearest_str = round(ltp_banknifty_at_916am/step)*step
nearest_str22 = round(ltp_banknifty_at_916am/step)*step
nearest_str=int(nearest_str/step)

otm_point=nearest_str
otm_point_pe=nearest_str
atm_strike=0
atm_strike_pe=0

max_value=nearest_str22*0.435
max_value_spread=nearest_str22*0.93333
max_loss_point=nearest_str22*0.083329
max_loss_point2=nearest_str22*0.1
ex='NFO'

h15=0
h11=0
ap=0
ap1=0
ap2=0
ap4=0
ap5=0
ap6=0
ap7=0
ap8=0
trail=0
trail2=0
tp=0
lp=0
kp=0
mp=0
sp=0
sp1=0
sp2=0
sp4=0
sp5=0
sp6=0
trail4=0
trail5=0
xp=0
xp2=0
no_ce=0
no_pe=0
er_trade=0
total_posi=0
ap11=0
sp11=0
sx=0
sy=0
sa=0
sb=0
sd=0
sf=0

time_add=datetime.datetime.now()
time_add6=datetime.datetime.now()
time_add2=datetime.datetime.now()
read_file=0
ce_trade=0
pe_trade=0

#swing variable
try:
    file1="cedataa.json"
    with open(file1, "r") as file:
        content = file.read()
        swing_ce_data = json.loads(content)

    spread_enter_ce=swing_ce_data['spread_enter_ce']
    spread_sl_ce=swing_ce_data['spread_sl_ce']
    scrip_long_ce=swing_ce_data['scrip_long_ce']
    scrip_shot_ce=swing_ce_data['scrip_short_ce']
    spread_ce_trail=swing_ce_data['spred_trail_ce']
    ce_trade=swing_ce_data['ce_trade']
    index_name=swing_ce_data['index_name']
    max_spread=swing_ce_data['spread_target']
    quantt=swing_ce_data['quant']
    option_four1=swing_ce_data['option_four1']
    exc_name=swing_ce_data['exc_name']

except Exception as e:
    ce_trade=0

try:
    file2="pedataa.json"
    with open(file2, "r") as file:
        content2 = file.read()
        swing_pe_data = json.loads(content2)
      
    spread_enter_pe=swing_pe_data['spread_enter_pe']
    spread_sl_pe=swing_pe_data['spread_sl_pe']
    scrip_long_pe=swing_pe_data['scrip_long_pe']
    scrip_shot_pe=swing_pe_data['scrip_short_pe']
    spread_pe_trail=swing_pe_data['spred_trail_pe']
    pe_trade=swing_pe_data['pe_trade']
    index_name=swing_pe_data['index_name']
    max_spread=swing_pe_data['spread_target']
    quantt=swing_pe_data['quant']
    option_four1=swing_pe_data['option_four1']
    exc_name=swing_pe_data['exc_name']
except Exception as e:
    pe_trade=0

xa=0
xb=0
xc=0
xd=0
xf=0
ya=0
yb=0
yc=0
yd=0
yf=0
da=0
db=0
dc=0
de=0
max_losss=2.5
time_add21=datetime.datetime.now()
time_add22=datetime.datetime.now()
main_trade=0

initi_pre=1001
time_add11=datetime.datetime.now()
intr_tra=0
intra1=0
modi_pe=0

data_index=objm.get_short_length_hist_data(name=name,exchange=exchange_name,interval="day",oi=True)
index_closing=data_index.iloc[-3]['close']
move=0
entry_tim=datetime.datetime.now()
sidein=0
km=0
kx=0

upside=0
dwside=0
up_time=datetime.datetime.now()
dw_time=datetime.datetime.now()
ema_trade=0
ema_tradepe=0
limit_mult=0.8

cash=kite.margins()['equity']['available']['opening_balance']
cash1=cash*0.5
if ce_trade==10 or pe_trade==10:
    cash=cash*1.031


while True:
    try:
        if h15==0 and datetime.datetime.now()>date_ext1('09:19:56') :
            if h11==0 and datetime.datetime.now()>entry_tim :
                try:
                    h11=10
                    if sidein==0:
                        ltp_banknifty_at_916am88=objm.get_data_for_single_script(exchange_name,name,"ltp")
                        if index_closing>ltp_banknifty_at_916am88:
                            move=-10
                        if index_closing<ltp_banknifty_at_916am88:
                            move=10
                        if (ltp_banknifty_at_916am88*0.001)>abs(index_closing-ltp_banknifty_at_916am88):
                            h11=0
                            entry_tim=datetime.datetime.now()+timedelta(seconds=59)
                            continue
                        sidein=10
                    
                    if move==10:
                        atm_ce=objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier =atm_strike, script_type="CE")
                        otm_ce11 = objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier = otm_point, script_type="CE")
                        one_lot=int(objm.get_lot_size(atm_ce)*1)
                        option_four=atm_ce[0:6]
                        dict1={"exchange": option_exchange,"transaction_type": "BUY","variety": "regular","product": "NRML","order_type": "MARKET","tradingsymbol":atm_ce,"quantity":one_lot}
                        dict4={"exchange": option_exchange,"transaction_type": "SELL","variety": "regular","product": "NRML","order_type": "MARKET","tradingsymbol":otm_ce11,"quantity":one_lot}
                        margin_detail2 = kite.basket_order_margins([dict1,dict4])
                        final_margin4=margin_detail2['initial']['total']

                        if ce_trade==10 or pe_trade==10:
                            sleep(1)
                            cash1=kite.margins()['equity']['available']['live_balance']

                        first_order_lot=math.floor(cash1/final_margin4)*one_lot
                        print(first_order_lot)
                        sleep(1)

                        ce_atm_price = objm.get_data_for_single_script(option_exchange,atm_ce,"ltp")
                        ce_otm_price = objm.get_data_for_single_script(option_exchange,otm_ce11,"ltp")
                        spread_ce_value=ce_atm_price-ce_otm_price
                    if h11==10 and move==10 and spread_ce_value>max_value and xp==0:
                        h11=0
                        xp=10
                        atm_strike=atm_strike+1
                        otm_point=otm_point+1
                        continue

                    if move==-10:
                        atm_pe=objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier = atm_strike_pe, script_type="PE") 
                        otm_pe11 = objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier = otm_point_pe, script_type="PE") 
                        one_lot=int(objm.get_lot_size(atm_pe)*1)
                        option_four=atm_pe[0:6]
                        dict2={"exchange": option_exchange,"transaction_type": "BUY","variety": "regular","product": "NRML","order_type": "MARKET","tradingsymbol":atm_pe,"quantity":one_lot}
                        dict5={"exchange": option_exchange,"transaction_type": "SELL","variety": "regular","product": "NRML","order_type": "MARKET","tradingsymbol":otm_pe11,"quantity":one_lot}
                        margin_detail2 = kite.basket_order_margins([dict2,dict5])
                        final_margin4=margin_detail2['initial']['total']

                        if ce_trade==10 or pe_trade==10:
                            sleep(1)
                            cash1=kite.margins()['equity']['available']['live_balance']
                            
                        first_order_lot=math.floor(cash1/final_margin4)*one_lot
                        print(first_order_lot)
                        sleep(1)

                        pe_atm_price = objm.get_data_for_single_script(option_exchange,atm_pe,"ltp")
                        pe_otm_price = objm.get_data_for_single_script(option_exchange,otm_pe11,"ltp")
                        spread_pe_value=pe_atm_price-pe_otm_price
                    if h11==10 and move==-10 and spread_pe_value>max_value and xp2==0:
                        h11=0
                        xp2=10
                        atm_strike_pe=atm_strike_pe+1
                        otm_point_pe=otm_point_pe+1
                        continue

                except Exception as e:
                    print('problem in margin finding part ', e)
                
                #ce spread value
            if h11==10 and move==10:
                ce_atm_price=objm.get_data_for_single_script(option_exchange,atm_ce,"quote")['depth']['buy'][0]['price']
                ce_otm_price=objm.get_data_for_single_script(option_exchange,otm_ce11,"quote")['depth']['sell'][0]['price']
                spread_ce_value=ce_atm_price-ce_otm_price
                
            if h11==10 and ap==0 and move==10 and datetime.datetime.now()<date_ext1('15:26:00'):
                ap=10
                spread_ce_value_excute=(ce_atm_price-ce_otm_price)-entry_decay
                spread_ce_sl=(spread_ce_value_excute-max_loss_point)
                spread_trail_ce=spread_ce_value_excute*1.84

                if max_loss_point<spread_ce_value_excute*0.25<max_loss_point2:
                    spread_ce_sl=(spread_ce_value_excute-(spread_ce_value_excute*0.25))
                if spread_ce_value_excute*0.25>=max_loss_point2:
                    spread_ce_sl=(spread_ce_value_excute-max_loss_point2)
                if ema_trade==11:
                    spread_ce_sl=spread_ce_value_excute-(max_loss_point)

                atm_ce_id=objm.place_order(tradingsymbol=atm_ce, transaction_type=kite.TRANSACTION_TYPE_BUY, order_type=kite.ORDER_TYPE_LIMIT, price=round(ce_atm_price*1.08,1), quantity=first_order_lot, product=kite.PRODUCT_NRML, exchange=option_exchange,  variety=kite.VARIETY_REGULAR,  validity=kite.VALIDITY_DAY,tag='ceatmid')
                sleep(1)
                otm_ce_id = objm.place_order(variety=kite.VARIETY_REGULAR, exchange=option_exchange, tradingsymbol=otm_ce11,transaction_type='SELL', quantity=first_order_lot, product=kite.PRODUCT_NRML, order_type=kite.ORDER_TYPE_LIMIT,price=round(ce_otm_price*0.92,1), validity=kite.VALIDITY_DAY,tag='ceotmid')
                sleep(21)
            if h11==10 and ap==10 and move==10 and sx==0 and date_ext1('09:24:00')<datetime.datetime.now() :
                orders_data = pd.DataFrame(objm.kite.orders())
                for index, row in orders_data.iterrows():
                    if row['tag']=='ceatmid' :
                        atm_ce_id=row['order_id']
                    if row['tag']=='ceotmid' :
                        otm_ce_id=row['order_id']
                sx=10
            if ap==10 and kp==0 and move==10 and  kite.order_history(atm_ce_id)[-1]['status']=='COMPLETE' and kite.order_history(otm_ce_id)[-1]['status']=='COMPLETE':
                kp=10
                sleep(1)
            if kp==0 and ap==10 and move==10 and  datetime.datetime.now()>date_ext1('09:31:00'):
                objm.market_over_close_all_order_expiry_partial(option_four=option_four,exc_name=option_exchange)
                h15=10
            if ap==10 and move==10 and spread_ce_sl>spread_ce_value and ap1==0 and datetime.datetime.now()>time_add :
                ap1=10
            
            if ap==10 and move==10 and spread_ce_value_excute*1.8<spread_ce_value and ap8==0 and datetime.datetime.now()>time_add:
                ap8=10   
            if ap==10 and move==10 and  ap8==10 and spread_ce_value<spread_ce_value_excute and datetime.datetime.now()>time_add:
                trail2=10
            if datetime.datetime.now()>time_add and move==10:
                time_add=datetime.datetime.now()+timedelta(seconds=59)

            if ap==10 and move==10 and spread_ce_value>max_value_spread and ap6==0:
                ap6=10
                   
            if (ap1==10 or ap6==10 or trail2==10 ) and tp==0 and kp==10  and move==10:
                tp=10
                exit_ce_id=objm.place_order(tradingsymbol=otm_ce11, transaction_type=kite.TRANSACTION_TYPE_BUY, order_type=kite.ORDER_TYPE_LIMIT, price=round(ce_otm_price*1.08,1), quantity=first_order_lot, product=kite.PRODUCT_NRML, exchange=option_exchange,  variety=kite.VARIETY_REGULAR,  validity=kite.VALIDITY_DAY)  
            if tp==10 and ap2==0 and move==10 and kite.order_history(exit_ce_id)[-1]['status']=='COMPLETE':
                ap2=10
                objm.place_order(variety=kite.VARIETY_REGULAR, exchange=option_exchange, tradingsymbol=atm_ce,transaction_type='SELL', quantity=first_order_lot, product=kite.PRODUCT_NRML, order_type=kite.ORDER_TYPE_LIMIT,price=round(ce_atm_price*0.92,1), validity=kite.VALIDITY_DAY)
                
            

            
                #pe spread value
            if h11==10 and move==-10:
                pe_atm_price=objm.get_data_for_single_script(option_exchange,atm_pe,"quote")['depth']['buy'][0]['price']
                pe_otm_price=objm.get_data_for_single_script(option_exchange,otm_pe11,"quote")['depth']['sell'][0]['price']
                spread_pe_value=pe_atm_price-pe_otm_price
                sleep(1)
                    
            if h11==10 and mp==0 and move==-10 and datetime.datetime.now()<date_ext1('15:26:00'):
                mp=10
                spread_pe_value_excute=(pe_atm_price-pe_otm_price)-entry_decay
                spread_pe_sl=(spread_pe_value_excute-max_loss_point)
                spread_trail_pe=spread_pe_value_excute*1.84

                if max_loss_point<spread_pe_value_excute*0.25<max_loss_point2:
                    spread_pe_sl=(spread_pe_value_excute-(spread_pe_value_excute*0.25))
                if spread_pe_value_excute*0.25>=max_loss_point2:
                    spread_pe_sl=(spread_pe_value_excute-max_loss_point2)
                if ema_tradepe==11:
                    spread_pe_sl=spread_pe_value_excute-(max_loss_point)
                atm_pe_id=objm.place_order(tradingsymbol=atm_pe, transaction_type=kite.TRANSACTION_TYPE_BUY, order_type=kite.ORDER_TYPE_LIMIT, price=round(pe_atm_price*1.08,1), quantity=first_order_lot, product=kite.PRODUCT_NRML, exchange=option_exchange,  variety=kite.VARIETY_REGULAR,  validity=kite.VALIDITY_DAY,tag='peatmid')
                sleep(1)
                otm_pe_id = objm.place_order(variety=kite.VARIETY_REGULAR, exchange=option_exchange, tradingsymbol=otm_pe11,transaction_type='SELL', quantity=first_order_lot, product=kite.PRODUCT_NRML, order_type=kite.ORDER_TYPE_LIMIT,price=round(pe_otm_price*0.92,1), validity=kite.VALIDITY_DAY,tag='peotmid')
                sleep(21)
            if h11==10 and mp==10 and move==-10 and sy==0 and date_ext1('09:24:00')<datetime.datetime.now() :
                orders_data = pd.DataFrame(objm.kite.orders())
                for index, row in orders_data.iterrows():
                    if row['tag']=='peatmid' :
                        atm_pe_id=row['order_id']
                    if row['tag']=='peotmid' :
                        otm_pe_id=row['order_id']
                sy=10
                   
            if mp==10 and lp==0 and move==-10 and  kite.order_history(atm_pe_id)[-1]['status']=='COMPLETE' and kite.order_history(otm_pe_id)[-1]['status']=='COMPLETE':
                lp=10
                sleep(1)
            if lp==0 and mp==10 and move==-10 and datetime.datetime.now()>date_ext1('09:31:00'):
                objm.market_over_close_all_order_expiry_partial(option_four=option_four,exc_name=option_exchange)
                h15=10

            if mp==10 and move==-10 and spread_pe_sl>spread_pe_value and sp==0 and datetime.datetime.now()>time_add2 :
                sp=10
                
            if mp==10 and move==-10 and spread_pe_value_excute*1.8<spread_pe_value and sp1==0 and datetime.datetime.now()>time_add2:
                sp1=10
            if mp==10 and move==-10 and sp1==10 and spread_pe_value<spread_pe_value_excute and datetime.datetime.now()>time_add2:
                trail4=10
            if datetime.datetime.now()>time_add2 and move==-10:
                time_add2=datetime.datetime.now()+timedelta(seconds=59)
  
            if mp==10 and move==-10 and spread_pe_value>max_value_spread and sp4==0:
                sp4=10
                   
            if (sp==10 or sp4==10 or trail4==10 ) and sp5==0 and lp==10 and move==-10 :
                sp5=10
                exit_pe_id=objm.place_order(tradingsymbol=otm_pe11, transaction_type=kite.TRANSACTION_TYPE_BUY, order_type=kite.ORDER_TYPE_LIMIT, price=round(pe_otm_price*1.08,1), quantity=first_order_lot, product=kite.PRODUCT_NRML, exchange=option_exchange,  variety=kite.VARIETY_REGULAR,  validity=kite.VALIDITY_DAY)  
            if sp5==10 and sp6==0 and move==-10 and kite.order_history(exit_pe_id)[-1]['status']=='COMPLETE':
                sp6=10
                objm.place_order(variety=kite.VARIETY_REGULAR, exchange=option_exchange, tradingsymbol=atm_pe,transaction_type='SELL', quantity=first_order_lot, product=kite.PRODUCT_NRML, order_type=kite.ORDER_TYPE_LIMIT,price=round(pe_atm_price*0.92,1), validity=kite.VALIDITY_DAY)
            
            if ap2==10 or sp6==10:
                h15=10

    except Exception as e:
        print('problem in main spread ', e)


    #EMA CODE 
    try:
        if datetime.datetime.now()>date_ext1('09:20:31')  and ema_tradepe==0 and ema_trade==0:
            index_data=objm.get_short_length_hist_data(name=name,exchange=exchange_name,interval="5minute",oi=True)
            index_data['ema200']= tb.EMA(index_data['close'], timeperiod=200)
            index_data['ema150']= tb.EMA(index_data['close'], timeperiod=150)
            index_price=index_data.iloc[-2] 

            if index_price['ema200']>index_price['high'] and index_price['ema150']>index_price['high'] and dwside==0 :
                dwside=10
                upside=0
                dw_time=datetime.datetime.now()+timedelta(seconds=11)
                if dw_time>up_time and km==0 and kx==0:
                    dwside=11
                    km=10

            if index_price['ema200']<index_price['low'] and index_price['ema150']<index_price['low'] and upside==0 :
                upside=10
                dwside=0
                up_time=datetime.datetime.now()+timedelta(seconds=11)
                if dw_time<up_time and kx==0 and km==0:
                    upside=11
                    kx=10
            
    except Exception as e:
        print('problem in ema data ',e)
    

    try:
        if (ap2==10 or sp6==10) and datetime.datetime.now()<date_ext1('15:26:00') and ema_tradepe==0 and ema_trade==0:
            
            #upside
            if upside==10 and up_time>datetime.datetime.now():
                ltp_banknifty_at_916am88=objm.get_data_for_single_script(exchange_name,name,"ltp")
                if xp==10:
                    atm_strike=atm_strike-1
                    otm_point=otm_point-1
                atm_ce=objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier =atm_strike, script_type="CE")
                otm_ce11 = objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier = otm_point, script_type="CE")
                ema_trade=10

            if dwside==10 and dw_time>datetime.datetime.now():
                ltp_banknifty_at_916am88=objm.get_data_for_single_script(exchange_name,name,"ltp")
                if xp2==10:
                    atm_strike=atm_strike-1
                    otm_point=otm_point-1
                atm_pe=objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier =atm_strike, script_type="PE")
                otm_pe11 = objm.get_otm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0,multiplier = otm_point, script_type="PE")
                ema_tradepe=10

        if ema_trade==10 :
            ce_atm_price=objm.get_data_for_single_script(option_exchange,atm_ce,"quote")['depth']['buy'][0]['price']
            ce_otm_price=objm.get_data_for_single_script(option_exchange,otm_ce11,"quote")['depth']['sell'][0]['price']
            spread_ce_value=ce_atm_price-ce_otm_price
            if (name=='NIFTY 50' or name=='NIFTY FIN SERVICE' or name=='SENSEX'):
                limit_mult=0.7

            if spread_ce_value<max_value*limit_mult:
                h15=0
                h11=10
                ap=0
                move=10
                sx=0
                kp=0
                ap1=0
                ap8=0
                trail2=0
                ap6=0
                tp=0
                ap2=0
                ema_trade=11

        if ema_tradepe==10:
            pe_atm_price=objm.get_data_for_single_script(option_exchange,atm_pe,"quote")['depth']['buy'][0]['price']
            pe_otm_price=objm.get_data_for_single_script(option_exchange,otm_pe11,"quote")['depth']['sell'][0]['price']
            spread_pe_value=pe_atm_price-pe_otm_price
            if (name=='NIFTY 50' or name=='NIFTY FIN SERVICE' or name=='SENSEX'):
                limit_mult=0.7
            
            if spread_pe_value<max_value*limit_mult:
                h15=0
                h11=10
                mp=0
                move=-10
                sy=0
                lp=0
                sp=0
                sp1=0
                trail4=0
                sp4=0
                sp5=0
                sp6=0
                ema_tradepe=11

    except Exception as e:
        print('problem in ema sell' ,e)

    
    try:
        if datetime.datetime.now()>date_ext1('15:28:31') and read_file==0:
            try:
                os.remove(file1)
            except Exception as e:
                pass    
            try:
                os.remove(file2)
            except Exception as e:
                pass    
            sleep(1)
            position = pd.DataFrame(objm.kite.positions()['net'])
            if move==10:
                for index, row in position.iterrows():
                    if row['tradingsymbol']==atm_ce and row['quantity']>0:
                        da=10
                    if row['tradingsymbol']==otm_ce11 and row['quantity']<0:
                        db=10
            if move==-10:
                for index, row in position.iterrows():
                    if row['tradingsymbol']==atm_pe and row['quantity']>0:
                        dc=10
                    if row['tradingsymbol']==otm_pe11 and row['quantity']<0:
                        de=10

            if tp==0 and da==10 and db==10 and move==10:
                long_ce={"spread_enter_ce": spread_ce_value_excute, "scrip_long_ce": atm_ce,"scrip_short_ce": otm_ce11,'spread_sl_ce':spread_ce_sl,'spred_trail_ce':spread_trail_ce,'ce_trade':10,'index_name':name,'spread_target':nearest_str22,'quant':first_order_lot,'option_four1':option_four,'exc_name':option_exchange}
                cedata="cedataa.json"    
                with open(cedata, "w") as file:
                    json.dump(long_ce, file)
            if sp5==0 and dc==10 and de==10 and move==-10:
                long_pe={"spread_enter_pe": spread_pe_value_excute, "scrip_long_pe": atm_pe,"scrip_short_pe": otm_pe11,'spread_sl_pe':spread_pe_sl,'spred_trail_pe':spread_trail_pe,'pe_trade':10,'index_name':name,'spread_target':nearest_str22,'quant':first_order_lot,'option_four1':option_four,'exc_name':option_exchange}
                pedata="pedataa.json"    
                with open(pedata, "w") as file:
                    json.dump(long_pe, file)  
            
            read_file=10   
            
    except Exception as e:
        print('problem in data dump  ',e)


    
    try:
        if ce_trade==10 and sa==0 and date_ext1('09:16:51')>datetime.datetime.now()>date_ext1('09:16:00'):
            position = pd.DataFrame(objm.kite.positions()['net'])
            for index, row in position.iterrows():
                if row['tradingsymbol']==scrip_long_ce:
                    sa=10
                if row['tradingsymbol']==scrip_shot_ce:
                    sb=10
        if ce_trade==10 and datetime.datetime.now()>date_ext1('09:17:01') and sa==10 and sb==10:
            ce_atm_swing=objm.get_data_for_single_script(exc_name,scrip_long_ce,"quote")['depth']['buy'][0]['price']
            ce_otm_swing=objm.get_data_for_single_script(exc_name,scrip_shot_ce,"quote")['depth']['sell'][0]['price']
            sleep(1)
            spread_ce_swing_value=ce_atm_swing-ce_otm_swing
            
            if spread_ce_swing_value>max_spread*0.93333:
                xa=10

            if spread_ce_swing_value<spread_sl_ce and datetime.datetime.now()>time_add21:
                xf=10

            if spread_ce_swing_value>spread_enter_ce*1.8 and datetime.datetime.now()>time_add21:
                xd=10
            if spread_ce_swing_value<spread_enter_ce and xd==10 and datetime.datetime.now()>time_add21:
                xd=11
            if datetime.datetime.now()>time_add21:
                time_add21=datetime.datetime.now()+timedelta(seconds=59)

            if (xa==10 or xd==11 or xf==10) and xb==0:
                xb=10
                exit_ce_swing_id=objm.place_order(tradingsymbol=scrip_shot_ce, transaction_type=kite.TRANSACTION_TYPE_BUY, order_type=kite.ORDER_TYPE_LIMIT, price=round(ce_otm_swing*1.08,1), quantity=quantt, product=kite.PRODUCT_NRML, exchange=exc_name,  variety=kite.VARIETY_REGULAR,  validity=kite.VALIDITY_DAY)  
            if xb==10 and xc==0 and kite.order_history(exit_ce_swing_id)[-1]['status']=='COMPLETE':
                xc=10
                objm.place_order(variety=kite.VARIETY_REGULAR, exchange=exc_name, tradingsymbol=scrip_long_ce,transaction_type='SELL', quantity=quantt, product=kite.PRODUCT_NRML, order_type=kite.ORDER_TYPE_LIMIT,price=round(ce_atm_swing*0.92,1), validity=kite.VALIDITY_DAY)
                ce_trade=11
        

        if pe_trade==10 and sd==0 and date_ext1('09:16:51')>datetime.datetime.now()>date_ext1('09:16:00'):
            position = pd.DataFrame(objm.kite.positions()['net'])
            for index, row in position.iterrows():
                if row['tradingsymbol']==scrip_long_pe:
                    sd=10
                if row['tradingsymbol']==scrip_shot_pe:
                    sf=10
        if pe_trade==10 and datetime.datetime.now()>date_ext1('09:17:01') and sd==10 and sf==10:

            pe_atm_swing=objm.get_data_for_single_script(exc_name,scrip_long_pe,"quote")['depth']['buy'][0]['price']
            pe_otm_swing=objm.get_data_for_single_script(exc_name,scrip_shot_pe,"quote")['depth']['sell'][0]['price']
            spread_pe_swing_value=pe_atm_swing-pe_otm_swing
            
            if spread_pe_swing_value>max_spread*0.93333:
                ya=10

            if spread_pe_swing_value<spread_sl_pe and datetime.datetime.now()>time_add22:
                yf=10

            if spread_pe_swing_value>spread_enter_pe*1.8 and datetime.datetime.now()>time_add22:
                yd=10
            if spread_pe_swing_value<spread_enter_pe and yd==10 and datetime.datetime.now()>time_add22:
                yd=11
            
            if datetime.datetime.now()>time_add22:
                time_add22=datetime.datetime.now()+timedelta(seconds=59)
            if (ya==10 or yd==11 or yf==10) and yb==0:
                yb=10
                exit_pe_swing_id=objm.place_order(tradingsymbol=scrip_shot_pe, transaction_type=kite.TRANSACTION_TYPE_BUY, order_type=kite.ORDER_TYPE_LIMIT, price=round(pe_otm_swing*1.08,1), quantity=quantt, product=kite.PRODUCT_NRML, exchange=exc_name,  variety=kite.VARIETY_REGULAR,  validity=kite.VALIDITY_DAY)  
            if yb==10 and yc==0 and kite.order_history(exit_pe_swing_id)[-1]['status']=='COMPLETE':
                yc=10
                objm.place_order(variety=kite.VARIETY_REGULAR, exchange=exc_name, tradingsymbol=scrip_long_pe,transaction_type='SELL', quantity=quantt, product=kite.PRODUCT_NRML, order_type=kite.ORDER_TYPE_LIMIT,price=round(pe_atm_swing*0.92,1), validity=kite.VALIDITY_DAY)
                pe_trade=11
        
        if  datetime.datetime.now()>date_ext1('15:28:31') and (ce_trade==10 or pe_trade==10):
            objm.market_over_close_all_order_expiry_partial(option_four=option_four1,exc_name=exc_name)
            ce_trade=11
            pe_trade=11
        
    except Exception as e:
        print('problem in swing trade  ',e)
    

    try:
        if datetime.datetime.now()>date_ext1('09:31:10'):
            position2 = pd.DataFrame(objm.kite.positions()['net'])
            number_posi=len(position2.index)
            if (number_posi!=0 and  number_posi!=2 and  number_posi!=4 and number_posi!=6):
                sleep(61)
                position2 = pd.DataFrame(objm.kite.positions()['net'])
                number_posi=len(position2.index)
                if (number_posi!=0 and number_posi!=2 and  number_posi!=4 and number_posi!=6):
                    objm.market_over_close_all_order_expiry()
                    break
    except Exception as e:
        print('problem in number of position  ',e)
    

    try:
        
        if datetime.datetime.now()<date_ext1('09:15:10'):
            print('Waiting for market to open ')
            continue
        
        pnl=objm.get_live_pnl()
        
        if h11==10 and sidein==10:
            pnl1=objm.get_live_pnl_partial(option_four=option_four)
            print('SAME DAY TRADE PNL   ',pnl1)
        if h11==10 and sidein==10 and  -pnl1>cash/100*2.5:
            sleep(11)
            pnl1=objm.get_live_pnl_partial(option_four=option_four)
            if -pnl1>cash/100*2.5:
                objm.market_over_close_all_order_expiry_partial(option_four=option_four,exc_name=option_exchange)
                h15=10

        if (ce_trade==10 or ce_trade==11 or pe_trade==10 or pe_trade==11):
            pnl2=objm.get_live_pnl_partial(option_four=option_four1)
            print('SWING PNL   ',pnl2)  
            max_losss=3.01
            if -pnl2>cash/100*2:
                sleep(11)
                pnl2=objm.get_live_pnl_partial(option_four=option_four1)
                if -pnl2>cash/100*2:
                    objm.market_over_close_all_order_expiry_partial(option_four=option_four1,exc_name=exc_name)
                    ce_trade=11
                    pe_trade=11

        orders_data = pd.DataFrame(objm.kite.orders())
        if len(orders_data.index)>51:
            sleep(1)
            objm.market_over_close_all_order_expiry()
            sleep(2)
            break
        if datetime.datetime.now()>date_ext1('15:29:31'):
            break 
        if cash/100*max_losss<-pnl:
            sleep(11)
            pnl=objm.get_live_pnl()
            if cash/100*max_losss<-pnl:
                objm.market_over_close_all_order_expiry()
                break    
        print('GROSS PNL   ',pnl)  
        
        sleep(0.5)
        if date_ext1('09:31:00')<datetime.datetime.now()<date_ext1('15:10:00') and datetime.datetime.now()>time_add6:
            time_add6=datetime.datetime.now()+timedelta(seconds=901)
            ltp_banknifty_at_916am88=objm.get_data_for_single_script(exchange_name,name,"ltp")
            futu=objm.get_atm(ltp=ltp_banknifty_at_916am88,underlying=name,expiry=0, script_type="CE")
            itm_price=objm.get_data_for_single_script(option_exchange,futu,"ltp")

            test_id=objm.place_order(tradingsymbol=futu, transaction_type=kite.TRANSACTION_TYPE_BUY, order_type=kite.ORDER_TYPE_LIMIT, price=round(itm_price*0.2,1), quantity=one_lot, product=kite.PRODUCT_NRML, exchange=option_exchange,  variety=kite.VARIETY_REGULAR,  validity=kite.VALIDITY_DAY)
            sleep(2)
            kite.cancel_order(variety=kite.VARIETY_REGULAR, order_id=test_id)

    except Exception as e:
        print('problem in pnl ', e)


va=0
vb=0
vc=0
vd=0
ve=0
while True:
    try:
        sleep(1)
        orders_data = pd.DataFrame(objm.kite.orders())
        if len(orders_data.index)>61:
            sleep(1)
            objm.market_over_close_all_order_expiry()
            sleep(2)
            break
        pnl=objm.get_live_pnl()
        if cash/100*3.5<-pnl and va==0:
            va=10
            objm.market_over_close_all_order_expiry()
        if cash/100*4<-pnl and vb==0:
            vb=10
            objm.market_over_close_all_order_expiry()
        if cash/100*4.5<-pnl and vc==0:
            vc=10
            objm.market_over_close_all_order_expiry()
        if cash/100*5<-pnl and vd==0:
            vd=10
            objm.market_over_close_all_order_expiry()
        if cash/100*6<-pnl and ve==0:
            ve=10
            objm.market_over_close_all_order_expiry()
        if datetime.datetime.now()>date_ext1('15:29:31'):
            break 

    except Exception as e:
        print('problem in mal loss exit a ',e)



