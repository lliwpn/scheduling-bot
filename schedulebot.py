#notes
    # implement try catch later for errors
    # listofTime, listofISV, listofLogin -> class data structures 

import discord
from discord.ext import commands, tasks
from discord.ui import Select, View

import time
import math
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='%', intents=intents)

bot.remove_command('help')

time_sync = False
nearest_hour = 0
nearest_day = 0
listofTime = [] # timers

listofEmotes = [":yellow_square:", ":purple_square:", ":green_square:", ":brown_square:", ":red_square:", ":blue_square:", ":orange_square:", ":stop_button:", ":white_square_button:", ":fireworks:", ":milky_way:", ":stars:", ":sunrise:", ":night_with_stars:", ":cityscape:"]
listofOwnership = []

listofTimeemotes = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:", ":one::one:"]

listofISV = []
listofLogin = []
orderlist = []

b = ":white_large_square:"
n = "\n"
w = ":black_large_square:"
header = ":calendar::pencil::one::two::three::four::five:"
grid = [[b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b],
        [b, b, b, b, b]]
sidebar = [[w, ":zero:"],
           [w, w],
           [w, ":one:"],
           [w, w],
           [w, ":two:"],
           [w, w],
           [w, ":three:"],
           [w, w],
           [w, ":four:"],
           [w, w],
           [w, ":five:"],
           [w, w],
           [w, ":six:"],
           [w, w],
           [w, ":seven:"],
           [w, w],
           [w, ":eight:"],
           [w, w],
           [w, ":nine:"],
           [w, w],
           [w, ":keycap_ten:"],
           [w, w],
           [":one:", ":one:"],
           [w, w]]


## external functions

def search_for_preexisting_time(user_id):
    
    counter = len(listofTime)
    preexisting_flag = False
    while ((counter > 0) and (preexisting_flag == False)):
        preexisting_flag = user_check_list(listofTime[len(listofTime) - counter], user_id)
        counter = counter - 1
    return preexisting_flag

def user_check_list(unpackaged_layerone_item, user_id):
    
    if unpackaged_layerone_item[0] == user_id:
        return True
    else:
        return False

def fetch_info(user_id):

    counter = len(listofTime)
    not_found_yet = True
    while ((counter > 0) and (not_found_yet == True)):
        if user_check_list(listofTime[len(listofTime) - counter], user_id) == True:
            return listofTime[len(listofTime) - counter]
        counter = counter - 1

def fetch_info_end(user_id):
    counter = len(listofTime)
    not_found_yet = True
    while ((counter > 0) and (not_found_yet == True)):
        if user_check_list(listofTime[len(listofTime) - counter], user_id) == True:
            temp_data_holder = listofTime[len(listofTime) - counter]
            listofTime.remove(listofTime[len(listofTime) - counter])
            return temp_data_holder
        counter = counter - 1

def schedule_processor(grid, minimum, maximum):
    schstr = ""
    for i in range(minimum, maximum):
        schstr += schedule_processor_layer2(grid[i], sidebar[i])
    return schstr

def schedule_processor_layer2(grid_row, sb_row):
    rowstr = ""
    for j in range(2):
        rowstr += sb_row[j]
    for i in range(5):
        rowstr += grid_row[i]
    rowstr += "\n"
    return rowstr

def display_times(minimum, maximum):
    timestr = ""
    for i in range(minimum, maximum):
        cur_processing_hour = nearest_hour + (i * 3600)
        timestr = timestr + listofTimeemotes[i] + f" - <t:{cur_processing_hour}:t>\n"
    return timestr

def display_ownerships():
    ownstr = ""
    for i in range(len(listofOwnership)):
        iteration = listofOwnership[i]
        ownstr = ownstr + iteration[1] + f' - {iteration[0]} ({iteration[2]}er)\n'
    return ownstr

def has_ownership(author):
    counter = len(listofOwnership)
    for i in range(counter):
        if check_author(author, listofOwnership[i]) == True:
            unpacked_data = listofOwnership[i]
            return unpacked_data[1]
    return False

def check_author(author, unpacked_data):
    if author == unpacked_data[0]:
        return True
    return False

def create_ownership(author, fort):
    emote = "empty"
    for j in range(len(listofEmotes)):
        owned_flag = False
        for i in range(len(listofOwnership)):
            if emote_preowned(listofEmotes[j], listofOwnership[i]) == True:
                owned_flag = True
        if owned_flag == False:
            emote = listofEmotes[j]
            listofOwnership.append([author, emote, fort])
            return emote
    if emote == "empty":
        return False

def emote_preowned(testing_emote, against_data):
    if testing_emote == against_data[1]:
        return True
    else:
        return False

def update_ownerships():
    temp_del = []
    for i in range(len(listofOwnership)):
        if emote_search(listofOwnership[i]) == False:
            temp_del.append(listofOwnership[i])
    for j in range(len(temp_del)):
        listofOwnership.remove(temp_del[j])

def emote_search(data):
    emote = data[1]
    for i in range(len(grid)):
        working_with_row = grid[i]
        for j in range(5):
            if working_with_row[j] == emote:
                return True
    return False

def searchisv(author):
    for i in range(len(listofISV)):
        unwrapped = listofISV[i]
        if unwrapped[0] == author:
            return True
    return False

def fetchisv(author):
    for i in range(len(listofISV)):
        unwrapped = listofISV[i]
        if unwrapped[0] == author:
            return unwrapped[1]

def replaceisv(author, isv):
    for i in range(len(listofISV)):
        unwrapped = listofISV[i]
        if unwrapped[0] == author:
            unwrapped[1] = isv
            listofISV[i] = unwrapped
            break

def replaceisvlogin(author, isv):
    for i in range(len(listofLogin)):
        unwrapped = listofLogin[i]
        if unwrapped[0] == author:
            unwrapped[1] = isv
            listofLogin[i] = unwrapped
            break

def searchlogin(author):
    for i in range(len(listofLogin)):
        unwrapped = listofLogin[i]
        if unwrapped[0] == author:
            return True
    return False

#---

def space_search(id):
    counter = 5
    unwrap = grid[id]

    while counter > 0:
        if unwrap[5 - counter] == b:
            return (5 - counter)
        counter = counter - 1
    return False

def specific_col_search(col, id): # for end, simple case
    id -= 1
    unwrap = grid[id]
    if unwrap[col] == b:
        return True
    else:
        return False

def check_for_overlap(col, startrow, endrow, emote):
    for i in range(startrow, endrow):
        unwrapped = grid[i]
        if unwrapped[col] != b and unwrapped[col] == emote:
            return 0
        elif unwrapped[col] != b:
            return 1
    return False

def makebooking(col, startrow, endrow, emote):
    global grid
    for i in range(startrow, endrow):
        unwrapped = grid[i]
        unwrapped[col] = emote
        grid[i] = unwrapped
    return grid

def no_overlap(col, startrow, endrow, emote):
    for i in range(startrow, endrow):
        unwrapped = grid[i]
        if unwrapped[col] != b:
            return False
    return True

def scan_grid(start_id, end_id, emote):
    for i in range(start_id, end_id):
        unwrapped = grid[i]
        for j in range(5):
            if unwrapped[j] == emote:
                return True
    return False

def delete_from_range(start_id, end_id, emote):
    global grid
    for i in range(start_id, end_id):
        unwrapped = grid[i]
        for j in range(5):
            if unwrapped[j] == emote:
                unwrapped[j] = b
        grid[i] = unwrapped
    return grid

## bot functions

@bot.event
async def on_ready():
    print('login')
    loop.start()

#sync
    # grid stack shift efficiency
@tasks.loop(seconds = 60)
async def loop():
    fetched_time = time.time()
    global nearest_hour, nearest_day, time_sync, listofLogin

    if nearest_hour != math.floor(fetched_time - (fetched_time % 3600)): # refresh
        del grid[0]
        del grid[0]
        grid.append([b, b, b, b, b])
        grid.append([b, b, b, b, b])

        update_ownerships()

    if nearest_day != math.floor(fetched_time - (fetched_time % 86400)):
        listofLogin = []
    
    nearest_hour = math.floor(fetched_time - (fetched_time % 3600))
    nearest_day = math.floor(fetched_time - (fetched_time % 86400))
    time_sync = True
    return nearest_hour, nearest_day, time_sync, listofLogin

#listener
@bot.listen('on_message')
async def listener(message):
    if message.author == bot.user:
        return

#intro
@bot.command()
async def help(ctx):

    if time_sync == True:
        sync_status = f'current hour: <t:{nearest_hour}:t>'
    else:
        sync_status = "time is not synced..."
    
    intro = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "welcome!", type = 'rich', description = f'schedulebot: a tiering assistant bot\n \n commands: \n``%starttimer`` - start tracking time :clock1: \n ``%checkprogress`` - check how long you\'ve been playing :stopwatch: \n ``%endtimer`` - stop tracking time :clock10: \n ``%schedule`` - view and edit the schedule :calendar: \n and more... (try ``%commands``!) \n \n {sync_status}')
    await ctx.send(embed = intro)

#commands embed
@bot.command()
async def commands(ctx):

    commands_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "bot commands", type = 'rich', description = "``%starttimer`` - start tracking time :clock1: \n ``%checkprogress`` - check how long you\'ve been playing :stopwatch: \n ``%endtimer`` - stop tracking time :clock10: \n \n``%schedule`` - view and edit the schedule :calendar: \n \n ``%isv`` - edit your isv :bookmark_tabs:\n``%isvorder`` - get an isv order :1234:\n``%roomrules`` - set up or view room rules :receipt:\n \n``%parkingtrack [current_points] [parking_goal]`` - see how much progress you've made to your parking goal :parking:")
    commands_embed2 = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "bot commands", type = 'rich', description = "WIP")

    class EmbedOne(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label = "<-", style = discord.ButtonStyle.blurple, disabled = True)
        async def idling(self, interaction: discord.Interaction, self_item):
            await interaction.response.defer()
    
        @discord.ui.button(label = "->", style = discord.ButtonStyle.blurple)
        async def switchembeds1(self, interaction: discord.Interaction, self_item):
            await interaction.message.edit(embed = commands_embed2, view = EmbedTwo())
            await interaction.response.defer()
            await EmbedTwo().wait()

    class EmbedTwo(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label = "<-", style = discord.ButtonStyle.blurple)
        async def switchembeds(self, interaction: discord.Interaction, self_item):
            await interaction.message.edit(embed = commands_embed, view = EmbedOne())
            await interaction.response.defer()
            await EmbedOne().wait()

        @discord.ui.button(label = "->", style = discord.ButtonStyle.blurple, disabled = True)
        async def idling(self, interaction: discord.Interaction, self_item):
            await interaction.response.defer()
    
    await ctx.send(embed = commands_embed, view = EmbedOne())
    await EmbedOne().wait()

#tiering start
    # list format [ctx.author, time.time()]
@bot.command()
async def starttimer(ctx):
    if search_for_preexisting_time(ctx.author) == False:
        
        snapshot_time = time.time()
        listofTime.append([ctx.author, snapshot_time])

        tierstart_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = 'starting time recorded! :stopwatch:', type = 'rich', description = "good luck tiering / have fun filling!")
        await ctx.send(embed = tierstart_embed)

    else:

        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like you've already got a timer going! use ``%endtimer`` to stop that one before starting another one.", type = 'rich')
        await ctx.send(embed = error_embed)

#checking progress
@bot.command()
async def checkprogress(ctx):
    if search_for_preexisting_time(ctx.author) == True:
        
        fetched_info = fetch_info(ctx.author) # returns entire [1, 2] format
        raw_seconds = time.time() - fetched_info[1]
        hours = math.floor(raw_seconds / 3600)
        minutes = math.floor((raw_seconds % 3600) / 60)
        seconds = math.floor((raw_seconds % 3600) % 60)

        progress_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = 'nice work! :thumbsup:', type = 'rich', description = f'you started at <t:{math.floor(fetched_info[1])}:F> \n you\'ve been playing for {hours} hours, {minutes} minutes, and {seconds} seconds.')
        await ctx.send(embed = progress_embed)

    else:

        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "you don't have a timer going right now! use ``%starttimer`` to start one.", type = 'rich')
        await ctx.send(embed = error_embed)

#tiering end
@bot.command()
async def endtimer(ctx):
    if search_for_preexisting_time(ctx.author) == True:

        fetched_info = fetch_info_end(ctx.author) # returns entire [1, 2, 3] format
        raw_seconds = time.time() - fetched_info[1]
        hours = math.floor(raw_seconds / 3600)
        minutes = math.floor((raw_seconds % 3600) / 60)
        seconds = math.floor((raw_seconds % 3600) % 60)

        tierend_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = 'have a good rest! :tea:', description = f'you started at <t:{math.floor(fetched_info[1])}:F> \n you played for {hours} hours, {minutes} minutes, and {seconds} seconds.', type = 'rich')
        await ctx.send(embed = tierend_embed)

    else:

        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "you don't have a timer going right now! use ``%starttimer`` to start one.", type = 'rich')
        await ctx.send(embed = error_embed)

#@bot.command()
#async def standby(ctx):
    

#schedule --------------
    # embed page flipping non-efficient time refreshes, regenerates every action
    # consider making different ones for different channels/servers?
class EmbedOne(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label = "<-", style = discord.ButtonStyle.blurple, disabled = True)
    async def idling(self, interaction: discord.Interaction, self_item):
        await interaction.response.defer()
    
    @discord.ui.button(label = "->", style = discord.ButtonStyle.blurple)
    async def switchembeds1(self, interaction: discord.Interaction, self_item):
        schedule_embed2 = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "schedule :notepad_spiral:", type = 'rich', description = f'{header}\n{schedule_processor(grid, 8, 16)} \n __legend (still vivid)__ \n {display_times(4, 8)} \n {display_ownerships()} \n ``%add`` | ``%dele``')
        await interaction.message.edit(embed = schedule_embed2, view = EmbedTwo())
        await interaction.response.defer()
        await EmbedTwo().wait()

class EmbedTwo(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label = "<-", style = discord.ButtonStyle.blurple)
    async def switchembeds1(self, interaction: discord.Interaction, self_item):
        schedule_embed1 = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "schedule :notepad_spiral:", type = 'rich', description = f'{header}\n{schedule_processor(grid, 0, 8)} \n __legend (still vivid)__ \n {display_times(0, 4)} \n {display_ownerships()} \n ``%add`` | ``%dele``')
        await interaction.message.edit(embed = schedule_embed1, view = EmbedOne())
        await interaction.response.defer()
        await EmbedOne().wait()

    @discord.ui.button(label = "->", style = discord.ButtonStyle.blurple)
    async def switchembeds2(self, interaction: discord.Interaction, self_item):
        schedule_embed3 = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "schedule :notepad_spiral:", type = 'rich', description = f'{header}\n{schedule_processor(grid, 16, 24)} \n __legend (still vivid)__ \n {display_times(8, 12)} \n {display_ownerships()} \n ``%add`` | ``%dele``')
        await interaction.message.edit(embed = schedule_embed3, view = EmbedThree())
        await interaction.response.defer()
        await EmbedThree().wait()

class EmbedThree(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label = "<-", style = discord.ButtonStyle.blurple)
    async def switchembeds1(self, interaction: discord.Interaction, self_item):
        schedule_embed2 = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "schedule :notepad_spiral:", type = 'rich', description = f'{header}\n{schedule_processor(grid, 8, 16)} \n __legend (still vivid)__ \n {display_times(4, 8)} \n {display_ownerships()} \n ``%add`` | ``%dele``')
        await interaction.message.edit(embed = schedule_embed2, view = EmbedTwo())
        await interaction.response.defer()
        await EmbedTwo().wait()

    @discord.ui.button(label = "->", style = discord.ButtonStyle.blurple, disabled = True)
    async def idling(self, interaction: discord.Interaction, self_item):
        await interaction.response.defer()

@bot.command()
async def schedule(ctx):

    schedule_embed1 = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "schedule :notepad_spiral:", type = 'rich', description = f'{header}\n{schedule_processor(grid, 0, 8)} \n __legend (still vivid)__ \n {display_times(0, 4)} \n {display_ownerships()} \n ``%add`` | ``%dele``')
       
    await ctx.send(embed = schedule_embed1, view = EmbedOne())
    await EmbedOne().wait()

#---

@bot.command()
async def add(ctx):

    starttime_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "how long are you planning on playing? :clock1:", type = 'rich', description = f'``%book [0 - 11] [0 or 30] [fill or tier] [0 - 12] [0 or 30]``\n *the first two numbers are your starting time and the last two are your end time \n \n{display_times(0, 11)}\n ``0`` if on the hour and ``30`` if at the half hour\n ``fill`` if filling and ``tier`` if tiering\n__try ``%addexample`` for help!__')
    await ctx.send(embed = starttime_embed)

@bot.command()
async def addexample(ctx):
    example_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "example booking", type = 'rich', description = "since the menu shows\n\n:nine: - 11:00 AM\n:keycap_ten: - 12:30 PM\n\n and i have time to fill then, i book that time with\n``%book 9 0 fill 10 30``")
    await ctx.send(embed = example_embed)

@bot.command()
async def book(ctx, starthour, startmin, fort, endhour, endmin):
    
    if (starthour.isdigit() == False or startmin.isdigit() == False or (fort != "fill" and fort != "tier") or endhour.isdigit() == False or endmin.isdigit() == False):
        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like your inputs weren't in the right format. try again?")
        await ctx.send(embed = error_embed)

    else:
        starthour = int(starthour)
        startmin = int(startmin)
        endhour = int(endhour)
        endmin = int(endmin)
    
        if (starthour < 0 or
            starthour > 11 or
            (startmin != 0 and startmin != 30) or
            endhour < 0 or
            endhour > 12 or
            (endmin != 0 and endmin != 30) or
            (endhour == 12 and endmin == 30)):

            error2_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like one of your time values was out of range. try again?")
            await ctx.send(embed = error2_embed)
        elif ((starthour > endhour) or (starthour == endhour and startmin > endmin)):

            error3_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like your starting time is before your ending time! try again?")
            await ctx.send(embed = error3_embed)

        else:

            emote = "empty"
            has = has_ownership(ctx.author)
            if type(has) == bool:
                create = create_ownership(ctx.author, fort)
                if type(create) == bool:
                    error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "the schedule has reached its current max capacity of 15 users.")
                    await ctx.send(embed = error_embed)
                else:
                    emote = create
            else:
                emote = has

            if (emote != "empty"):
                startslot_id = starthour * 2
                if startmin == 30:
                    startslot_id = startslot_id + 1
                endslot_id = endhour * 2
                if endmin == 30:
                    endslot_id = endslot_id + 1 # row ids

                acc_start = math.floor(nearest_hour + (startslot_id * 1800))
                acc_end = math.floor(nearest_hour + (endslot_id * 1800))

                if scan_grid(startslot_id, endslot_id, emote) == True:
                    error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like you've already signed up for an overlapping time! maybe doublecheck and try again?")
                    await ctx.send(embed = error_embed)
                else:
                    startplace_column = space_search(startslot_id)
                    if type(startplace_column) != bool:
                        if (specific_col_search(startplace_column, endslot_id) == True) and (no_overlap(startplace_column, startslot_id, endslot_id, emote) == True):
                            makebooking(startplace_column, startslot_id, endslot_id, emote)
                            
                            confirm_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "success! :white_check_mark:", type = 'rich', description = f'you\'re now booked as a {fort}er from <t:{acc_start}:F> to <t:{acc_end}:F>')
                            await ctx.send(embed = confirm_embed)
                        elif (specific_col_search(startplace_column, endslot_id) == True) and (no_overlap(startplace_column, startslot_id, endslot_id, emote) == False):
                            while startplace_column < 5:
                                startplace_column += 1
                                if no_overlap(startplace_column, startslot_id, endslot_id, emote) == True:
                                    
                                    makebooking(startplace_column, startslot_id, endslot_id, emote)

                                    confirm_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "success! :white_check_mark:", type = 'rich', description = f'you\'re now booked as a {fort}er from <t:{acc_start}:F> to <t:{acc_end}:F>')
                                    await ctx.send(embed = confirm_embed)
                                    
                                    break
                                if startplace_column == 5:
                                    err_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like the slots for that time are full!")
                                    await ctx.send(embed = err_embed)
                        #else:
                            #search for closest time to end
                    #else:
                        #if (space_search(endslot_id).isdigit() == True):
                            #search for closest start time and book
                        #else:
                            #find closest end time. consider slant booking case. ask for confirm

#delete intro
@bot.command()
async def dele(ctx):
    delete_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "deleting a booking :pencil:", type = 'rich', description = f'``%deletebook [0 - 11] [0 or 30] [0 - 12] [0 or 30]``\n *the first two digits are the start times of the clear and the last two digits are the end times of the clear')
    await ctx.send(embed = delete_embed)

#del
@bot.command()
async def deletebook(ctx, starthour, startmin, endhour, endmin):

    if (starthour.isdigit() == False or startmin.isdigit() == False or endhour.isdigit() == False or endmin.isdigit() == False):
        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like your inputs weren't in the right format. try again?")
        await ctx.send(embed = error_embed)

    else:
        starthour = int(starthour)
        startmin = int(startmin)
        endhour = int(endhour)
        endmin = int(endmin)
    
        if (starthour < 0 or
            starthour > 11 or
            (startmin != 0 and startmin != 30) or
            endhour < 0 or
            endhour > 12 or
            (endmin != 0 and endmin != 30) or
            (endhour == 12 and endmin == 30)):

            error2_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like one of your time values was out of range. try again?")
            await ctx.send(embed = error2_embed)
        elif ((starthour > endhour) or (starthour == endhour and startmin > endmin)):

            error3_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "it looks like your starting time is before your ending time! try again?")
            await ctx.send(embed = error3_embed)
        else:
            has = has_ownership(ctx.author)
            if type(has) == bool:
                error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", type = 'rich', description = "looks like you don't have any time slots to delete! try making some with ``%add``.")
                await ctx.send(embed = error_embed)
            else:

                start_id = starthour * 2
                if startmin == 30:
                    start_id += 1
                end_id = endhour * 2
                if endmin == 30:
                    end_id += 1
                
                delete_from_range(start_id, end_id, has)

                acc_start = math.floor(nearest_hour + (start_id * 1800))
                acc_end = math.floor(nearest_hour + (end_id * 1800))

                confirm_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "success! :white_check_mark:", type = 'rich', description = f'any slots you booked from <t:{acc_start}:F> to <t:{acc_end}:F> have been deleted.')
                await ctx.send(embed = confirm_embed)        
    
#-----------------------

#isv set
@bot.command()
async def isv(ctx):
    if searchisv(f'{ctx.author}') == False:
        setup_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "let's get your isv set up! :tools:", description = "what's your current team isv? please enter it in the format ``xxx/yyy``, where ``xxx`` is your leader's internal score value and ``yyy`` is your team's total internal score value. if you need help, check out #guides or ask for help!\n\n**note: remember to login with ``%login`` daily in order to be shown in ``%roomorder``!**", type = 'rich')
        await ctx.send(embed = setup_embed)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        try:
            m_msg = await bot.wait_for("message", check=check, timeout = 60)
            msg = str(m_msg.content)

            if (len(msg) != 7) or (msg[0].isdigit() == False or msg[1].isdigit() == False or msg[2].isdigit() == False or msg[3] != "/" or msg[4].isdigit() == False or msg[5].isdigit() == False or msg[6].isdigit() == False):
                error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like your isv wasn't in the right format.", type = 'rich')
                await ctx.send(embed = error_embed)
            else:
                listofISV.append([f'{ctx.author}', msg])
                conf_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "success! :white_check_mark:", description = f'your isv has been saved as {msg}', type = 'rich')
                await ctx.send(embed = conf_embed)
        except asyncio.TimeoutError:
            err2_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like you timed out! try again?", type = 'rich')
            await ctx.send(embed = err2_embed)
                    
    else:
        
        class EmbedView(discord.ui.View):
            def __init__(self):
                super().__init__()
            
            @discord.ui.button(label = "update isv", style = discord.ButtonStyle.blurple)
            async def switchembeds(self, interaction: discord.Interaction, self_item):
                setup_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "let's get your isv up to date! :tools:", description = "what's your current team isv? please enter it in the format ``xxx/yyy``, where ``xxx`` is your leader's internal score value and ``yyy`` is your team's total internal score value\n\n**note: remember to login with ``%login`` daily in order to be shown in ``%roomorder``!**", type = 'rich')
                await interaction.message.edit(embed = setup_embed, view = None)
                await interaction.response.defer() # del maybe
                
                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel
                try:
                    msg = await bot.wait_for("message", check=check)
                    msg = str(msg.content)

                    if (len(msg) != 7) or (msg[0].isdigit() == False or msg[1].isdigit() == False or msg[2].isdigit() == False or msg[3] != "/" or msg[4].isdigit() == False or msg[5].isdigit() == False or msg[6].isdigit() == False):
                        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like your isv wasn't in the right format.", type = 'rich')
                        await ctx.send(embed = error_embed)
                    else:
                        replaceisv(f'{ctx.author}', msg)

                        if searchlogin(f'{ctx.author}') == True:
                            replaceisvlogin(f'{ctx.author}', msg)
                        
                        conf_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "success! :white_check_mark:", description = f'your isv has been saved as {msg}', type = 'rich')
                        await ctx.send(embed = conf_embed)
                except asyncio.TimeoutError:
                    err2_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like you timed out! try again?", type = 'rich')
                    await ctx.send(embed = err2_embed)
        
        recorded_isv = fetchisv(f'{ctx.author}')
        hm_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "looks like you've already got an isv! :scroll:", description = f'it\'s saved as {recorded_isv}', type = 'rich')
        await ctx.send(embed = hm_embed, view = EmbedView())
        await EmbedView().wait()

@bot.command()
async def login(ctx):
    if searchisv(f'{ctx.author}') == False:
        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like your isv isn't logged yet! add it with ``%isv``", type = 'rich')
        await ctx.send(embed = error_embed)
    elif searchlogin(f'{ctx.author}') == True:
        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like you're already logged in for today! all good", type = 'rich')
        await ctx.send(embed = error_embed)
    else:
        listofLogin.append([f'{ctx.author}', fetchisv(f'{ctx.author}')])
        conf_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "success! :white_check_mark:", description = "you've logged in for today!", type = 'rich')
        await ctx.send(embed = conf_embed)

#isv order
@bot.command()
async def isvorder(ctx):

    class SongSelect(discord.ui.Select):
        def __init__(self):
            options = [discord.SelectOption(label = "hitoenvy expert", value = 0),
                       discord.SelectOption(label = "hitoenvy hard", value = 1),
                       discord.SelectOption(label = "melt expert", value = 2),
                       discord.SelectOption(label = "melt hard", value = 3)]
            super().__init__(placeholder = "select the song you'll be playing", options=options)

        async def callback(self, interaction: discord.Interaction):

            def isvconv(orderlist):
                order_isv = ['', '', '', '', '']
                def num_conv(isv):
                    isv = str(isv)
                    leadisv = int(isv[0] + isv[1] + isv[2])
                    fullisv = int(isv[4] + isv[5] + isv[6])
                    isvp = ((fullisv - leadisv) * 0.2) + leadisv
                    return isvp
                
                for i in range(len(orderlist)):
                    order_isv[i] = num_conv(fetchisv(orderlist[i]))
                return order_isv

            def ordering(listisv):
                def inorder(listp):
                    if listp[0] >= listp[1] and listp[1] >= listp[2] and listp[2] >= listp[3] and listp[3] >= listp[4]:
                        return True
                    else:
                        return False
                while inorder(listisv) == False:
                    for j in range(len(listisv)):
                        if j == 0 or j == 4:
                            continue
                        else:
                            if listisv[j] > listisv[j - 1]:
                                temp1 = listisv[j]
                                temp2 = listisv[j - 1]
                                listisv[j] = temp2
                                listisv[j - 1] = temp1
                            elif listisv[j] < listisv[j + 1]:
                                temp1 = listisv[j]
                                temp2 = listisv[j + 1]
                                listisv[j] = temp2
                                listisv[j + 1] = temp1
                return listisv

            def set_to_song(listisv, song_val):
                final_order = ['', '', '', '', '']
                song_val = int(song_val)
                if song_val == 0: # 3 2 1 4 5
                    final_order[0] = listisv[2]
                    final_order[1] = listisv[3]
                    final_order[2] = listisv[4]
                    final_order[3] = listisv[1]
                    final_order[4] = listisv[0]
                elif song_val == 1: # 3 2 4 1 5
                    final_order[0] = listisv[2]
                    final_order[1] = listisv[3]
                    final_order[2] = listisv[1]
                    final_order[3] = listisv[4]
                    final_order[4] = listisv[0]
                elif song_val == 2: # 1 2 4 5 3
                    final_order[0] = listisv[4]
                    final_order[1] = listisv[3]
                    final_order[2] = listisv[1]
                    final_order[3] = listisv[0]
                    final_order[4] = listisv[2]
                elif song_val == 3: # 1 4 3 5 2
                    final_order[0] = listisv[4]
                    final_order[1] = listisv[1]
                    final_order[2] = listisv[2]
                    final_order[3] = listisv[0]
                    final_order[4] = listisv[3]
                return final_order

            def organizenmd(names, orderedisvs):
                def matchnametoisv(names, isv):
                    for j in range(len(names)):
                        working_isv = fetchisv(names[j])
                        leadisv = int(working_isv[0] + working_isv[1] + working_isv[2])
                        fullisv = int(working_isv[4] + working_isv[5] + working_isv[6])
                        isvp = ((fullisv - leadisv) * 0.2) + leadisv
                        if isv == isvp:
                            return names[j]
                namelist = []
                for i in range(len(orderedisvs)):
                    name = matchnametoisv(names, orderedisvs[i])
                    namelist.append(name)
                    names.remove(name)
                return namelist
            
            orderisv = set_to_song(ordering(isvconv(orderlist)), self.values[0]) # resulting order
            ordernm = organizenmd(orderlist, orderisv)
            order_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "here you go!", description = f'your order is: \n\n :red_square::regional_indicator_p::one: - {ordernm[0]}\n:yellow_square::regional_indicator_p::two: - {ordernm[1]}\n:green_square::regional_indicator_p::three: - {ordernm[2]}\n:blue_square::regional_indicator_p::four: - {ordernm[3]}\n:purple_square::regional_indicator_p::five: - {ordernm[4]}', type = 'rich')
            await interaction.response.edit_message(embed = order_embed, view = None)
        
    class SelectView2(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(SongSelect())

#---

    class MemberSelect(discord.ui.Select):
        
        def __init__(self):
            options = []
            super().__init__(placeholder = "select the members in the room", max_values = 5, min_values = 5, options=options)
            
        async def callback(self, interaction: discord.Interaction): # issue
            global orderlist
            orderlist = [self.values[0], self.values[1], self.values[2], self.values[3], self.values[4]]
            song_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "which song are you ordering for? :musical_note:", type = 'rich')
            await interaction.response.edit_message(embed = song_embed, view = SelectView2())
            await SelectView2().wait()

            return orderlist

    def memseledit():
        working = MemberSelect()
        for i in range(len(listofLogin)):
            unwrapped = listofLogin[i]
            working.append_option(discord.SelectOption(label = f'{unwrapped[0]}', description = f'{unwrapped[1]}'))
        return working

    class SelectView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(memseledit())

    if (len(listofLogin) < 5):
        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "it looks like there aren't enough people logged in yet!", type = 'rich')
        await ctx.send(embed = error_embed)
    else:
        choice1_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "which members are playing? :man_dancing:", type = 'rich')
        await ctx.send(embed = choice1_embed, view = SelectView())
        await SelectView().wait()

#parking progress
@bot.command()
async def parkingtrack(ctx, cur, pkg):
    if ((pkg.isdigit() == True) and (cur.isdigit() == True)):
        pkg = int(pkg)
        cur = int(cur)

        if cur > pkg:
            huh_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "whoa!", description = "looks like you overshot... new plan?", type = 'rich')
            await ctx.send(embed = huh_embed)
            
        elif cur == pkg:
            congrats_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "congrats! :tada:", description = "rest well!", type = 'rich')
            await ctx.send(embed = congrats_embed)

        else:
            parking_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "keep on going! :coffee:", type = 'rich', description = f'you\'re ``{round(cur * 100 / pkg, 2)}%`` to your parking goal of ``{pkg}`` pts. you\'ve got this!')
            await ctx.send(embed = parking_embed)

    else:

        error_embed = discord.Embed(colour = discord.Color.from_rgb(171, 213, 237), title = "oops!", description = "looks like the inputs weren't numbers.", type = 'rich')
        await ctx.send(embed = error_embed)

#----------------------------------------------------------------------------

bot.run("token here")
