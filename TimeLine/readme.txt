This is the readme for the app development process. Hopefully I come back to this if I ever forget what it is
I'm doing with this project or why.

First, the reason. I was tired of feeling like I had dozens and dozens of goals banging around in my mind.
All of them were disorganized, and there was no real timeline to them. Some things needed to be done today,
while others could be done in small chunks over the next few years. I needed some way to differentiate those.

Second, you can't accomplish what you don't admit you want. Having a tangible list of goals is infinitely 
more valuable than letting them float around in your head. Back to point one, it becomes totally unmanageable 
when you have a list that's a thousand items long.

I currently keep a rough draft of this project on a whiteboard in my apartment. It has its pros and cons. On
the plus side, it's extremely easy to initialize: just make a table with columns labeled "Today", "2 Days",
"10 Days", "30 Days", "100 Days", "500 Days", "2000 Days", and "> 2000 Days". There's no barrier to entry for
this particular technique, other than a $20 whiteboard. It also has the benefit of being constantly visible.

But there are cons to this method too. Putting goals in these columns requires a name and a date. If a
particular goal doesn't have a built-in "due date" but I know I want to accomplish it wtihin the next 100 days,
I need to take a few seconds to figure out when a hundred days from now is so that I have a range of viable
dates. Also, if today is Jan_1 and a due date is Jan_4, that goal will be in the "10 Days" column; I'll need to
manually move it into the "2 Days" column tomorrow.

There are lots of other downsides to having this info on a whiteboard in your home. It's not portable, it's not
easily added to on a whim (especially when you're away from home, unless you're really good about writing 
yourself notes and following up on them), and it's not even a little bit private. Anyone who enters my home can
see my entire list of goals, but it beats the current alternative, which is that I don't admit them in a 
tangible way, and therefore never achieve them.

A possible solution to this would be an Excel spreadshehet. I actually have one of those in this form right
now. I keep it on my Google Drive, so it's theoretically accessible whenever I have an internet connection. 
But this has downsides as well:

1) my Drive contains a lot of stuff I wouldn't want other people to see. Nothing bad, but private things like
writing samples, personal info, notes to myself, etc. So it's less than ideal to make that directory 
vulnerable every time I want to leave myself a quick reminder to get milk or something trivial.

2) usually you'll be on a personal computer, so Drive vulnerability isn't much of an issue. But it's still
not ideal; I actually don't think that Excel is perfect for this application, and Google Sheets is 
obviously even less capable than Excel.

3) adding to the above point, a spreadsheet isn't great for this. I don't want to open up a spreadsheet every
time I want to leave myself a little reminder. Also, I have no idea how to make the items in the columns move
as today's date changes.

Ideally, what I need is an app. It would be something that could sync between phone and computer, and it would
have its own command line. Assuming today's date is Jan_1, it would take simple arguments like "bookshelf 11" 
and convert them into "Bookshelf (January 12)". As you can see, the second argument is the number of days until
it's "due".

This second argument can have two forms, integer or date. In integer form (like the above example), the program
automatically calculates the date on which it would land. Python seems to have some pretty solid methods built
into the time and datetime modules for this, which I've played around with a little. In date form, the user
simply inputs the date (in a specific format at first, but hopefully it will be able to parse any standard
format eventually) and the program assigns it as the due date.

The second argument can also be left out. In this case, the item gets placed on in the "Today" column, yielding
a reminder at the end of the day for the user to either check it off or assign it a date.

Items on this moving list of lists can have their dates changed as well. The important part about this app
isn't necessarily to get everything you've ever dreamed of accomplished as soon as possible; it's to admit to 
yourself what it is that you actually do want to accomplish. The time frame is, in the end, up to the user.
Dates can be moved forward and backward--however, if a date is moved backward three times, that item will show
up in red from now on. This is to deter users from keeping items on the list indefinitely that they think they
want to accomplish but actually show no willingness or desire to do the things necessary to accomplish them.

Goals can be marked "complete" or "abandoned." Obviously, only the user will know which of these is true.
Abandoned goals will be erased from the app. Completed goals will go into a log with their completion date. The
user can access this log at any time to see how much they've accomplished, and what column each goal was in when
it was first scheduled, in order to confer a bit of weight to these accomplishments.

At the end of every day, the app should ask about progress on "2 Days" goals. Every third day, ask about the 
"10 Days" goals. Every tenth day, ask about the "30 days" goals, etc.
