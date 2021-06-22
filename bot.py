import logging
from telegram import( 
    InlineQueryResultArticle, 
    InputTextMessageContent, 
    Update,InlineKeyboardButton, 
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    InlineQueryHandler,
    CallbackQueryHandler,
)
from uuid import uuid4
import mysql.connector
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#YOU HAVE TO DO FILL IT YOUR SELF 
mydb = mysql.connector.connect(
    host="localhost",
    user="",
    password="",
    database=""
)
mydb.ping(True)
mycursor = mydb.cursor()
######################
CHANNEL='shareer'
STICKER,NAMESTICKER , GIF,NAMEGIF = range(4)
PHOTO,NAMEPHOTO , VIDEO,NAMEVIDEO=range(4)
def start(update: Update, context: CallbackContext):
    delete = lambda context: context.job.context.delete()
    param = context.args
    if not param : 
        
        start= ("سلام... 👋"
                "\n-برای افزودن استیکر از 👈 /addsticker "
                "\n-برای افزودن گیف از 👈 /addgif "
                "\n-برای افزودن عکس از 👈 /addphoto "
                "\n-برای افزودن ویدیو از 👈 /addvideo "
                "\n-اطلاعات بیشتر /info"
                "\n اگر دوست دارید ویژگی های جدید ربات را از دست ندهید در این کانال به آدرس https://t.me/erunpie جوین شوید 😉"
        )
        update.message.reply_text(start)
    elif param[0] =='add':
        update.message.reply_text('یا این ربات می توانید پس افزودن یک رسانه به صورت اینلاین لینک پیام را به اشتراک بگذارید برای دریافت لیست دستورات از /list ')
    else: 
        try: 
           #(type, name, fileid)
           mycursor.execute("SELECT type, name, fileid FROM saver WHERE fileuniqueid='%s' AND status = 'True'"%param[0])
           myresult = mycursor.fetchone()
           if not myresult :
               update.message.reply_text('چنین چیزی در حال حاضر موجود نمی باشد شاید حذف شده باشد.')
           else:
               if myresult[0] == 'sticker' :
                    message=context.bot.send_sticker(chat_id= update.effective_user.id, sticker=myresult[2])
                    message_2=context.bot.send_message(chat_id= update.effective_user.id , text= myresult[1]+'\n\n بعد از 30 ثانیه حذف میشود')
                    
               if myresult[0] == 'gif' :
                    message=context.bot.send_animation(chat_id= update.effective_user.id , animation =myresult[2])
                    message_2=context.bot.send_message(chat_id= update.effective_user.id , text= myresult[1]+'\n\n بعد از 30 ثانیه حذف میشود')
               if myresult[0] == 'photo' :
                    message=context.bot.send_photo(chat_id= update.effective_user.id , photo =myresult[2])
                    message_2=context.bot.send_message(chat_id= update.effective_user.id , text= myresult[1]+'\n\n بعد از 30 ثانیه حذف میشود')
               if myresult[0] == 'video' :
                    message=context.bot.send_video(chat_id= update.effective_user.id , video =myresult[2])
                    message_2=context.bot.send_message(chat_id= update.effective_user.id , text= myresult[1]+'\n\n بعد از 30 ثانیه حذف میشود')
               context.job_queue.run_once(delete, 30, message)
               context.job_queue.run_once(delete, 30, message_2)
        except:
           pass
#sticker
def add_sticker(update: Update, context: CallbackContext):
    user =update.effective_user.id
    mycursor.execute("SELECT type, name, fileid FROM saver WHERE status ='True' AND user ='%s'"%user)
    myresult = mycursor.fetchall()
    if len(myresult) == 40:
        update.message.reply_text('بیشتر از مجکوع 40 گیف و استیکر نمی توانید آپلود کنید با استفاده از /del چند گزینه را پاک کنید ')
        return ConversationHandler.END 
    else:
        context.user_data['type'] = 'sticker'
        update.message.reply_text(' حالا استیکر را ارسال کنید یا /cancel')
        return STICKER
def get_sticker(update: Update, context: CallbackContext):   
    context.user_data['fileid'] = update.message.sticker.file_id
    context.user_data['fileuniqueid']= update.message.sticker.file_unique_id
    update.message.reply_text('حالا عنوان استیکر رو وارد کنید')
    return NAMESTICKER
#gif
def add_gif(update: Update, context: CallbackContext):
    user =update.effective_user.id
    mycursor.execute("SELECT type, name, fileid FROM saver WHERE status ='True' AND user ='%s'"%user)
    myresult = mycursor.fetchall()
    if len(myresult) == 40:
        update.message.reply_text('بیشتر از مجکوع 40 گیف و استیکر نمی توانید آپلود کنید با استفاده از /del چند گزینه را پاک کنید ')
        return ConversationHandler.END
    else:
        context.user_data['type'] = 'gif'
        update.message.reply_text('حالا گیف را ارسال کنید یا /cancel')
    return GIF
def get_gif(update: Update, context: CallbackContext):
    context.user_data['fileid'] = update.message.animation.file_id
    context.user_data['fileuniqueid']=update.message.animation.file_unique_id
    update.message.reply_text('حالا عنوان گیف را وارد کنید')
    return NAMEGIF
#photo
def add_photo(update: Update, context: CallbackContext):
    user =update.effective_user.id
    mycursor.execute("SELECT type, name, fileid FROM saver WHERE status ='True' AND user ='%s'"%user)
    myresult = mycursor.fetchall()
    if len(myresult) == 40:
        update.message.reply_text('بیشتر از مجکوع 40 گیف و استیکر نمی توانید آپلود کنید با استفاده از /del چند گزینه را پاک کنید ')
        return ConversationHandler.END
    else:
        context.user_data['type'] = 'photo'
        update.message.reply_text('حالا عکس را ارسال کنید یا /cancel')
    return PHOTO
def get_photo(update: Update, context: CallbackContext):
    context.user_data['fileid'] = update.message.photo[0].file_id
    context.user_data['fileuniqueid']=update.message.photo[0].file_unique_id
    update.message.reply_text('حالا اسم عکس را وارد کنید')
    return NAMEPHOTO

#video
def add_video(update: Update, context: CallbackContext):
    user =update.effective_user.id
    mycursor.execute("SELECT type, name, fileid FROM saver WHERE status ='True' AND user ='%s'"%user)
    myresult = mycursor.fetchall()
    if len(myresult) == 40:
        update.message.reply_text('بیشتر از مجکوع 40 گیف استیکر عکس و ویدیو نمی توانید داشته باشید با استفاده از /del چند گزینه را پاک کنید ')
        return ConversationHandler.END
    else:
        context.user_data['type'] = 'video'
        update.message.reply_text('حالا ویدیو را ارسال کنید یا /cancel')
    return GIF
def get_video(update: Update, context: CallbackContext):
    context.user_data['fileid'] = update.message.video.file_id
    context.user_data['fileuniqueid']=update.message.video.file_unique_id
    update.message.reply_text('حالا اسم ویدیو را وارد کنید')
    return NAMEGIF
def get_name(update: Update, context: CallbackContext):
    context.user_data['name']=update.message.text
    try : 
      sql = "INSERT INTO saver (user, type, name ,fileid, fileuniqueid, status ) VALUES (%s, %s, %s,%s,%s,%s )"
      val = (update.effective_user.id,context.user_data['type'],context.user_data['name'],context.user_data['fileid'],context.user_data['fileuniqueid'],'True')
      mycursor.execute(sql, val)
      mydb.commit()
      key_board_3=[
                     [InlineKeyboardButton('ارسال' , switch_inline_query ="")],
                    ]
      context.bot.send_message(chat_id =update.effective_user.id , text ='افزوده شد برای استفاده روی دکمه زیر کلیک کنید.',reply_markup = InlineKeyboardMarkup(key_board_3))
    except : 
        context.bot.send_message(chat_id =update.effective_user.id , text ='شکست خورد')
    return ConversationHandler.END

def delete(update: Update, context: CallbackContext):
    user = update.effective_user.id
    mycursor.execute("SELECT  name,type, fileuniqueid FROM saver WHERE status ='True' AND user ='%s'"%str(user))
    myresult = mycursor.fetchall()
    #[(name,type,fileuniqueid)]
    if not myresult:
        context.bot.send_message(chat_id =update.effective_user.id , text = 'درحال حاضر چیزی برای حذف کردن ندارید')
    else:
        key_board=[]
        for i in myresult:
             key_board.append([InlineKeyboardButton(i[0]+' - '+i[1] ,callback_data =i[2])])     
        context.bot.send_message(chat_id =update.effective_user.id , text = 'یک مورد را انتخاب کنید: ',reply_markup= InlineKeyboardMarkup(key_board))

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    try :
      mycursor.execute("UPDATE saver SET status = 'False' WHERE fileuniqueid = '%s'"% query.data)
      mydb.commit() 
      query.edit_message_text('حذف شد!')
    except: 
        pass

def search_engine(user):
    mydb.ping(True)
    mycursor.execute("SELECT type, name, fileuniqueid FROM saver WHERE status ='True' AND user ='%s'"%str(user))
    myresult = mycursor.fetchall()
    if not myresult:
        guide = [('-','چگونه استفاده کنیم؟','add')]
        return guide
    else:
        return myresult    
def inlinequery(update:Update, context:CallbackContext):
    inline_results = list()
    user = update.effective_user.id
    # [(type , name , fileuniqueid ),()]
    try :
       results = search_engine(user)
    except:
       results={'DATABASE HAS ENCOUNTERED A PROBLEM :(':'BAACAgQAAxkBAAICcGC38ZIjHuMDOgsHru9UGcPyHMxzAAJhCgAC-O3AUbroA8GXMt0jHwQ'}
    for i in results :
        url ='https://t.me/%s?start=%s'%(CHANNEL,i[2])
        key_board_2=[
                [InlineKeyboardButton('دیدن' , url =url)],
        ]
        inline_results.append(InlineQueryResultArticle(id=uuid4(),
                                                       title= i[1] ,
                                                       input_message_content= InputTextMessageContent(' عنوان: %s \n نوع: %s\n' %(i[1],i[0])),
                                                       description='نوع: '+i[0],
                                                       reply_markup= InlineKeyboardMarkup(key_board_2)
                                                                    ))

    update.inline_query.answer(inline_results[:40],cache_time=0)



def cancel(update: Update, context: CallbackContext) :
    update.message.reply_text('کنسل شد')
    return ConversationHandler.END

def list_bot(update: Update, context: CallbackContext):
    update.message.reply_text('-/addgif\n-/addsticker\n-/addphoto\n-/addvideo\n-/info')
def info(update: Update, context: CallbackContext) :
    update.message.reply_text('This is really simple bot wich is written by | @e_run_pie | \nIf you want source code  visit : \nhttps://github.com/erunpie/inline-video')
    
        
def main():

    updater = Updater("1814261032:AAF3LsbYB1gjOVFHhzy_9MlqX8pOKcyqN8c")

    dispatcher = updater.dispatcher

    #sticker
    sticker_handler = ConversationHandler(
        entry_points=[CommandHandler('addsticker',add_sticker ,run_async=True) ],
        states={
            STICKER: [MessageHandler(Filters.sticker , get_sticker, run_async=True)],
            NAMESTICKER: [MessageHandler(Filters.text & ~Filters.command ,get_name, run_async=True)],        
        },
        fallbacks=[CommandHandler('cancel',cancel ,run_async=True)],  
    )
    dispatcher.add_handler(sticker_handler)

    #gif
    gif_handler = ConversationHandler(
        entry_points=[CommandHandler('addgif',add_gif ,run_async=True) ],
        states={
            GIF: [MessageHandler(Filters.animation , get_gif, run_async=True)],
            NAMEGIF: [MessageHandler(Filters.text & ~Filters.command ,get_name, run_async=True)],        
        },
        fallbacks=[CommandHandler('cancel',cancel ,run_async=True)],  
    )
    dispatcher.add_handler(gif_handler)

    #photo
    photo_handler = ConversationHandler(
        entry_points=[CommandHandler('addphoto',add_photo,run_async=True) ],
        states={
            PHOTO: [MessageHandler(Filters.photo , get_photo, run_async=True)],
            NAMEPHOTO: [MessageHandler(Filters.text & ~Filters.command ,get_name, run_async=True)],        
        },
        fallbacks=[CommandHandler('cancel',cancel ,run_async=True)],  
    )
    dispatcher.add_handler(photo_handler)

    #video
    video_handler = ConversationHandler(
        entry_points=[CommandHandler('addvideo',add_video ,run_async=True) ],
        states={
            VIDEO: [MessageHandler(Filters.video , get_video, run_async=True)],
            NAMEVIDEO: [MessageHandler(Filters.text & ~Filters.command ,get_name, run_async=True)],        
        },
        fallbacks=[CommandHandler('cancel',cancel ,run_async=True)],  
    )
    dispatcher.add_handler(video_handler)


    dispatcher.add_handler(CallbackQueryHandler(button, run_async=True))
    dispatcher.add_handler(CommandHandler("start", start, run_async=True))
    dispatcher.add_handler(CommandHandler("del", delete, run_async=True))
    dispatcher.add_handler(CommandHandler("list", list_bot, run_async=True))
    dispatcher.add_handler(CommandHandler('info',info ,run_async=True))
    dispatcher.add_handler(InlineQueryHandler(inlinequery, run_async=True))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
