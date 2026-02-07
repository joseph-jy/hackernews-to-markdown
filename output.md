fd# [OpenCiv3: Open-source, cross-platform reimagining of Civilization III](https://openciv3.org/)

- “Mac will try hard not to let you run this; it will tell you the app is damaged and can’t be opened and helpfully offer to trash it for you. From a terminal you can xattr -cr /path/to/OpenCiv3.app to enable running it.”

How far OSX has come since the days of the “cancel or allow” parody advert.
    - Mac support is the bane of my existence. It doesn't help that none of us core contributors have one, so if anyone is willing to be a lab monkey...
        - I have a Macbook Pro M4 Max, an Apple Developer account, a bit of time, and some enthusiasm. Would love to help!
            - Notarize it.
        - Apple has been slowly tightening the screws on app notarization (code signing) requirements for running apps on macOS. To do it properly you need to be a registered developer ($100/year), and they're certainly not making it easy if you don't have access to a Mac.

[https://support.apple.com/guide/security/app-code-signing-pr...](https://support.apple.com/guide/security/app-code-signing-process-sec3ad8e6e53/web)>On devices with macOS 10.15, all apps distributed outside the App Store must be signed by the developer using an Apple-issued Developer ID certificate (combined with a private key) and notarized by Apple to run under the default Gatekeeper settings.Re: Developer ID Certificates:https://developer.apple.com/help/account/certificates/create...I suspect the friction that users are facing are due to dodging the above requirements.
        - You can run macOS in a docker container. There’s no hardware acceleration for gpu, but works well enough.

You can also try macinabox if you have unraid:https://hub.docker.com/r/spaceinvaderone/macinaboxIt’s probably the easiest way of setting up a Mac VM if you have unraid. I know there are similar options for qemu and kvm based hypervisors. If you have an amd gpu you should be able to pass it through.
            - quickemu [1] is good at running macOS VMs.

1:[https://github.com/quickemu-project/quickemu](https://github.com/quickemu-project/quickemu)
            - My only experience with docker is headless in CI. I do have AMD. I'll have to look into this. Thanks
            - Emulating mac or using mac SDKs on non apple devices is against apple's bullshit license though.
                - BS needs to be countered with rejection.
        - Why not build it as a web app and play via browser?
    - What is going on with this? I tried that and the alias I have built in for this problem, `make_safe() { xattr -d -r com.apple.quarantine $1 }`

The application cannot be opened for an unexpected reason, error=Error Domain=RBSRequestErrorDomain Code=5 "Launch failed." UserInfo={NSLocalizedFailureReason=Launch failed., NSUnderlyingError=0xae1038720 {Error Domain=NSPOSIXErrorDomain Code=163 "Unknown error: 163" UserInfo={NSLocalizedDescription=Launchd job spawn failed}}}
        - The situation is actually worse than it looks.

This error exists because Apple has effectively made app notarization mandatory, otherwise, users see this warning. In theory, notarization is straightforward: upload your DMG via their API, and within minutes you get a notarized/stamped app back.…until you hit the infamous "Team is not yet configured for notarization" error.Once that happens, you can be completely blocked from notarizing your app for months. Apple has confirmed via email that this is a bug on their end. It affects many developers, has been known for years, and Apple still hasn't fixed it. It completely elimiates any chances of you being able to notarize your app, thus, getting rid of this error/warning.Have a loot at how many people are suffering from this for years with no resolution yet:https://developer.apple.com/forums/thread/118465
            - Yikes. Why anyone would willingly develop for Apple platforms is beyond me. But then I also don't understand why some some people like using the crap^WmacOS. To each their own I guess. Hardware does look nice though, too bad about their software.
                - Because they "have" to have the nice display or good battery life I guess. Everyone has different priorities. Personally for me it's Linux or nothing.
                - Because that is where the users with the money are.
                - Well, gotta sell wherever the customers are, unfortunately.
        - And it inspired me to buy it for $0.99 and that doesn't work on Mac either. The [your least favorite tribe] really are revolting.
    - "cancel or allow" (which Microsoft still does) makes no sense, it just trains user to click "allow" every time. Users don't know what they should allow or not.

It makes a bit more sense on accounts that have a password set, as it requires you to confirm identity when introducing significant changes to the system (and this is something that Apple also does).Gatekeeper is a different thing, it basically makes sure that the software you're trying to run has been pre-scanned for malware by a trusted party, similar to Windows's "smart screen" and Defender or APt's GPG keyring integration. It's a mechanism that is completely invisible to 99+% of users. If you see a Gatekeeper pop-up and the app in question is not mlaware, the developer is doing something very wrong.
    - To be fair, the threat landscape changed, too.
        - Not terribly fair. When Windows decided running everything as administrator was bad and to add a visual sudo-like prompt, Apple made fun of them for it, but it was Microsoft reacting to a changing threat landscape then too.
            - UAC is not a security boundary. Malware can bypass it if it wants.
                - It helps to actually enable having to type a password instead of clicking on Yes.

However yes, security is much more than an UAC dialog.
            - Vista gets maligned but UAC is a good feature to have around, and Vista introduced it.
                - My first thought was "But back then those prompts were constant, making them almost useless", though maybe that did actually help by making software vendors rely less on admin rights?
                    - That was the whole point.
        - I mean it has, but the situation is getting ridiculous, I'm at the point where I'm honestly not sure what special set of magical incantations and rituals I need to do to get this process to work, it seems to change between different bits of software and get more complex with time as if Apple keeps finding proverbial bigger fools who can get through this mess without intending to and so they're solution is to keep making it increasingly more Byzantine

The thing that really irks me is I've got a paid developer account with Apple, I've already done the xcode dance, notarized binaries and all that nonsense, shouldn't this have activated some super special bit on my Apple account that says“this one needs to do random stuff now and again and after saying, `Hey just checking in, doing this will do X to your computer probably, and maybe set it on fire, but if you say "go for it, I promise I know what I'm doing', I'm gonna trust you champ`,finger guns“(not sure why in my head the personification of Apple would do "finger guns", but here we are I guess :shrug:)Hell at this point I'll take a checkbox in my settings that says, ”Some people are into extreme sports, I love to install random binaries, just get out of my way“
            - You shouldn't need the company's permission to run whatever you want on your machine.
                - It's not an issue of permission, it's an issue of trying to make a computer that's safe for grandma to use. Criminals can and will convince grandma to navigate a byzantine labyrinth of prompts and technical measures in order to drain her bank account. That's the threat model we're dealing with here.
                    - I think a time-lock feature to enable “I know what I’m doing mode” for a year, after a 48h delay would be ok.

Or something like that
                        - I like Chrome OS's approach where you essentially choose your security level at initial setup, and need to wipe your machine if you wish to change it.
                        - No, that would still suck.
                    - We should have never tried to let grandma on computers. Wait until the genAI revolution is complete (2027) and she can entirely use her voice and an AI agent in natural language to do things. This but unironically. Gate keeping is very good and keeps enshittification at bay. We see what happens when Apple tried to let in too many normies and wouldn't let them get darwin awards.

Answer to Skeltoac: Isaiah 57:1
                        - I helped my mother out with a computer, gave her a mac after she called twic a wee about a windows popup. Eventually she became a grandmother, and later in old age, with dementia she stlll using the mac more or less successfully to google and e-mail.
Intentionality, coordination are important for keeping cognitive faculty.
It all sounds so easy, but letting her send e-mail through voice could create confusing situations.
                        - We are all creeping toward old age. Let’s be kind to our future selves.
                        - No thanks.
                        - Who's to say the criminals won't use a genAI agent to call grandma and social-engineer her so they can drain her bank account?
                            - They pretty much already are.
                        - This attitude is worse than Apple’s.
                - And you don't. THIs is not iOS, gatekeeper can be bypassed if you know how.
                - …you don’t, just like you don’t need the bank’s permission to withdraw funds… but they will still try and stop you pulling out $10,000 so you can buy iTunes gift cards to pay off your taxes.
            - IIRC everything you compile on macOS yourself, possibly only when using Apple’s llvm toolchain, already gets the proper bits set to execute just fine. This also seems to work for rust and go binaries. I’m not sure whether that is because they replicated the macOS llvm toolchain behaviour for the flag or whether another mechanism is at play.
    - This is the reason I dropped macOS as a platform target. Apple will make users think you're a hacker trying to trick them, because macOS acts as if your app is radioactive if you don't pay the Apple tax, and refuses to let users run the apps they want.

Maybe 1 out of 1,000 users will know the magic ritual required to run what they want on their machine, and for every one of those, 10,000 are gaslit into thinking you were trying to harm them by macOS' scary warnings and refusal to do what they want.
    - I got a Mac only because of the excellent battery life. But I dread Os X. Not only it is dumbed down and it is harder to accomplish what is trivial in other operating system, but I have to actively fight against it if I want to run software that is not downloaded from the app store or I want to open files with apps I downloaded from elsewhere. And the UI is broken.
- Civ III is still my go-to activity for long flights with no internet - I've yet to find a better way to instantly time-travel forward 12 hours.

I haven't tried OpenCiv3, but I'm glad it exists - getting vanilla Civ III running on MacOS is a hassle and still has issues with e.g. audio and cutscenes. I also hope it leads to a way to improve worker automation. Managing your workers well is important, doing it manually is tedious, and the built-in Automate feature is really bad.
    - It

to be Factorio for me (I live in Australia, so long flights happen a lot). The problem with Factorio the flight isn't long enough! and the game bleeds into 100+ hours post-flight.
        - Dwarf Fortress. That's

how to suddenly say "Oh, how did it get to 4am already?"
    - I like Civilization games but they make 4hrs feel like 30min, so I can’t play them. Otherwise it would be the year 2060 already
        - I feel like my last words could be ‘just one more turn’.
        - Can we settle for Factorio and 2028?
        - Yes, exactly
I had to stop myself starting the game after 7 else I don't sleep
    - How do you manage the laptop + mouse?
        - track point
    - How did I not ever think to do this? Such a good idea.
    - Yeah civ VI on my iPad with an apple pencil kills flights
    - The key here is seeing this mentioned and not time traveling forward until 6 AM Saturday morning.
        - Yeah, that's what Factorio is for.
            - Factorio is a game about bird songs.
            - Sleep is the bottleneck.
            - You won’t get me this time.
    - > I've yet to find a better way to instantly time-travel forward 12 hours

I find it very hard to use a computer in the cramped tables of the plane. And the person in front always ends up aggressively reclining only when I have a laptop out. Plus I feel bad that maybe my bright light is disturbing the people sleeping next to me.
        - It amazes me that high paid SV techies won’t pay more to fly in premium or business
            - I remember being a high paid techie getting 19 hours of paid work done between Melbourne and New York, on a laptop in economy (and a long layover in LAX due to a storm). It was fricking glorious, most productive day of my life.
            - Business class flights from Sydney to San Francisco cost A$6k, 6-10x as much as economy. Flights from Sydney to Europe are more like 3-4x (A$7k vs A$2k) but still ludicrously expensive. Good luck convincing your company to expense that for work trips, and most of us don't have SV salaries. Honestly, I still manage to get some work done on long flights, the more annoying thing is flights which don't have power outlets or WiFi.

If you are a point hacker you could spend the points on upgrades (which tend to give you better rates than buying base tickets) but then you're paying for a minor comfort improvement that you wouldn't pay for normally -- which is a textbook example of induced consumption and is playing into exactly how airlines want you to use points.
            - It’s incredibly expensive on international flights, right? A 12 hour flight sounds like something that would cost thousands for business class.
    - There goes my weekend…
    - The total war games are like civilization but with actually good combat. Especially if you get mods like DEI for Rome 2, RTR for Rome 1 remastered, etc. It's regrettable that we let the grimdark warhammer crowd define the series.

The paradox grand strategy games are like civilization but with real agency and at times straight up historical accuracy.Meanwhile I have to deal with Ghandi actually nuking everyone (the bug is ACTUALLY REAL IN CIV 5, the best modern civ game!). Not sure why Indians aren't mad as hell at the whole series.
        - I have found paradox games to have uneven game mechanics; some run miles wide, some of them run deep, and many others are just very superficial, and there is no reliable indication which will be which when you are playing fresh.
            - Check out Terra Invicta.

It's like the modern-era Paradox game you wanted but all the mechanics synergize with each other.Unfortunately it's abittoo complicated as a result.
- Hi all, OpenCiv3 founder here. Thanks for the support! Check us out on Civfanatics or Discord to keep up with the project.
    - Any interesting insights about using Godot with C#? I love C# and I'm happy using it in Godot even though it's not as seamless as in Unity: in Godot 4 we still can't export to Web if the project is C#, and there's the whole conversion between C# types and Godot types that adds inefficiencies and extra allocations, etc.; it feels like it's a second-class language in Godot.

I'm always interested in seeing what people find when developing larger projects in C#.
        - We were building on C# Godot and I think it is a second class citizen in the sense that 1) you can't export to wasm and 2) they are moving the interface to be handled by gdextension.

That said, I think once you get the gist of it and understand the landmines, it is really nice to use vanilla dotnet rather than unity's fork.
        - The founding developers were all software engineers with .NET experience, so it was the natural choice even though at the time it was Godot 3.x with Mono. I had used Unity before but not Godot. The project is structured as mostly plain C# DLLs with a relatively thin Godot UI layer controlling it, so the Godot type system is fairly encapsulated. We haven't really seen any issues with those decisions beyond just working out the communication between Godot and DLL. But again we were just working from what we knew so I can't really say if this was the best way to go about it.
    - Oh my, this brings me back! One of my fondest gaming memories involves a massive Civilization 3 PBEM match between a number of Civilization fan sites, where we all had private forums and ran these virtual nations against each other. This was way back in 2002 or 2003!

I believe Civfanatics was in it (run by “Chieftess” if I recall), Apolyton (which I was a member of — elected in as Minister of Public Works and had to come up with a plan to clear our pesky jungles) and a number of other sites.It was such an awesome time. Real diplomacy and trade negotiations between the fan sites while waiting to play our turns. Man, it was fun.
        - I was also there at Civfanatics watching from the sidelines. Fond memories indeed, and some of those same people laid the foundations for this project.
        - I didn’t do that stuff but I remember…was it Kryten? Making a multi unit graphic utility, I used it to make and publish some multi units. Fun times. CivFanatics was great.
    - Would it be feasible to add an API to OpenCiv3 (or run it as an SDK) so we can script up actions?
        - There will certainly at least be (technically already is) a Lua scripting interface for mods. We've hand-waved some talk of a proper C# SDK but have no concrete plans yet.
    - Have you considered adding LLM features for the negotiations? Could be cool.
        - From what I've seen with projects like this, the successful ones do a good job of 'sticking to the mission' of faithfully recreating the original game in a modern engine (openMW, daggerfall unity, all my points of reference are TES related)

The neat part is that they are open source, so anyone who wants to take it in a different direction can fork it. The multiplayer version openMW being a great example of this.
        - you may be interested in

[https://www.paxhistoria.co/](https://www.paxhistoria.co/)
            - No information on the website, but a login. Suspicious.
        - not sure if serious...
            - Even if you don't want an LLM for the actual functionality of negotiations, LLM-generated text would be neat. As-is, the text becomes irrelevant, "Our words are backed with nuclear weapons" is just "nukes = true" - letting an LLM tell you the AI has nukes seems like harmless fun.
            - Lifelong Civ player. I have always felt the negotiations part of the game is laughably bad, and a huge missed opportunity. The ability to use language as a tool -- diplomacy, but also rhetoric, veiled threats, etc -- is something I excel at, and I would love the chance to test my mettle against an enemy in an imaginary nuclear war context, because when else do you get to play high stakes games like that with words in real life? Civ is the perfect venue for it, but the game designers are extremely boneheaded about how they executed that particular part of the game.
        - You are getting downvoted, but this is a cool idea. Diplomacy has historically been a weak part of the series, and being able to shore that up may be a lot of fun to play against.
            - I would say diplomacy is the most misunderstood feature of the series. Players constantly

they want a stronger AI that's smarter at diplomacy. But whenever they have built an AI like that, their play testers complained that it doesn't behave like a real world leader (too ruthless).

This experience led Soren Johnson (co-designer of Civ III and lead designer of Civ IV) to the realization that Civ AIs are supposed to "play to lose" [1].[1]https://www.youtube.com/watch?v=IJcuQQ1eWWI
                - That makes sense, but at the end of the day, it may be more fun to play around with opponents that act more relatedly. This could take the form of in-game/session-appropriate diplomatic responses that don't read like pre-canned text, or, having explanatory text for why the AI is acting perhaps in goofy ways (which comes up a lot).
                - I am so tired of game designers/developers being so pathetically wrong about stuff like this. Modders have to CONSTANTLY fix these boneheaded, user hostile decisions in nearly every game. A lot of game developers are not the people actually loving/playing their games in the same way that the cello maker is usually not the cello player.

Even many popular mods fuck this up! DEI in Total War Rome 2 needssubmodsto make the AI play by the same rules as the player!!! This is top of the most subscribed list right now FOR A REASON!!![https://steamcommunity.com/sharedfiles/filedetails/?id=36258...](https://steamcommunity.com/sharedfiles/filedetails/?id=3625804410)Make the AI play by the exact same rules as the player. Make a scaling AI difficulty slider which goes from "piss easy" to "insane grandmaster" but without cheats. It's not that hard to do this, the chess engine crowd figured it out back in 2001. FEAR figured it out in 2004. Game AI has straight up not improved and at many times gotten worse in the ensuing two decades.
                    - They really didn't. No one likes playing against weaker chess engines. They play perfectly like a higher-rated engine and then randomly make an obvious blunder. They don't play naturally like a human player of that rating.The weaker AIs in Civ games do a far better job at "playing to lose" than low rated chess engines. It's not even close!
            - Maybe ask Ghandi for his favorite scone recipe, so that he won’t nuke you.
                - Gandhi*
- I love that the community is doing this, though I'm curious why Civ 3 in particular. My understanding was that "classic" (for lack of a better term) Civ fans tend to prefer either 2 or 4, and that 3 was considered to be not as good. But perhaps I was mistaken as to the community's opinions on the games.
    - I can definitely vouch for the 2 or 4 narrative, those have always been my favorites of the 'Modernish' civ games, but my favorite will always be CivNet (Civ 1 with multiplayer). There is some real simplicity in Civ 1 that makes it much better suited to a multiplayer experience than the later entries. It is a real pain to get any non-hotseat multiplayer working nowawdays, but well-worth it.
        - Agree, wish there were quality of life improvements to Civ1 that kept the simplicity and aesthetics fully intact, while modernizing some of the tedious mid/late game stuff like managing each city in a large empire based on some straightforward goals like 'more science' or 'fastest path to rocketry' or whatnot.

Freeciv unfortunately has none of the charm of Civ1.
        - I love civ 1 so so much.
    - For me the most classic one is Civ III by a mile. 4 was way too modern/ flashy for me and 2 too old school. But maybe I was just born at the right time for 3.
        - You can turn off a lot of the Civ 4 flash and it will feel more like Civ III.

But to each his own. Civ 4 was the first one that really, really hooked me.
            - For me it was Civ 4's modability that made it the best for me. Because when I got tired of playing Civ 4's normal game, I could install the Fall From Heaven mod and play a completely different game. Wizards, golems, angels, demons, spells, wild animals instead of barbarians (which could be tamed and turned into your own units if you had units with the right promotions)... it made for a completely different gameplay experience.

If I hadn't quit computer games cold turkey (when I realized I was showing all the signs of addiction) over a decade ago, I would still have Civ IV installed and still be playing it today. It just didn't get old, because of how varied the game could become.
    - Here's a perspective on "why civ 3" by one of the best civ 3 players:

[https://youtu.be/IOvWgfZiHGo?si=uvTWTaRQsfxE_ffN](https://youtu.be/IOvWgfZiHGo?si=uvTWTaRQsfxE_ffN)
        - Thank you for the link. It is enlightening for someone who likes to play the game, but is not obsessive about a particular version. (I like the idea of Civilization, and will play it for that reason alone. More often than not, I will choose an older version simply because it is faster to load and play than for the intrinsic merits of the ruleset itself.)
    - FreeCiv covers civ 1 and 2 more or less.

Personally, I didn't play much of 2 or 3, so I don't have strong feelings either way.
        - UnCiv covers civ 5 as well so I think there's a place for something in between

especially since openciv3 aims to fix some of civ 3's shortcomings
        - Freeciv's point of interest is that it's not trying to exactly replicate any one of the original Civs: it has its default ruleset plus others that are closer to the original games, but it's very easy to make your own.
            - Which FreeCiv? The one you install locally, or the one you play via browser on the Web?

[https://freecivweb.com/](https://freecivweb.com/)The latter has more, like Multiplayer 2.4 Dragoon, and Multiplayer 2.5 Elephant(in development), which weren't available locally when I last looked.There is alsohttps://github.com/longturn/freeciv21which has an acceptable local client, and finally does not slow down so much when playing larger maps with many AIs, like both FreeCiv and FreeCivWeb tend to do.https://longturn.readthedocs.io/en/latest/index.htmlI tried that, recently, andbarely espcapeda relapse. (Phew!)
    - Because it was born out of the Civ3 modding community which has been wanting a remake for 20+ years.

Sounds like you've been listening to Civ4 fans. ;) 3 is just as active on steam and has a very active and loyal multiplayer league.
        - Fair enough, thanks!
    - 3 is my favorite in the series, but maybe that's not a popular take.
    - civ 5 is now the most popular among hardcore civ fans. still in the top 100 games on steam. more than 2x the player count of its sequel
        - It is a great game, and the Vox Populi mod has given it so much more life.

VP has hands down the best AI that the Civ series has ever seen. My "wow" moment was when the enemy parachuted to my hinterlands to pillage my critical resources. In comparison, the official AI couldn't even pull off an amphibious attack.
    - I must admit that there is a certain sense of nostalgia I get from playing Civ 3 that I never got from any of the other Civ games, but that's probably just because it was the first Civ game I played and got really hooked on as a young kid.
    - > with capabilities inspired by the best of the 4X genre and lessons learned from modding Civ3. Our vision is to make Civ3 as it could have been

Looks to not be a straight remake. I wonder whether 3 is a preferable target because things like graphical complexity in >= 4 is too much.
        - Well, "capabilities" is carrying a lot of weight there. One of the main objectives is to design it for unrestricted modding to accommodate all of the wishlisted features, but "out of the box" the default game mode will be 1:1 in mechanics with some QoL improvements. The inspiration is mostly for designing systems in a way that can be easily reconfigured or extended to behave in other ways. We hope that by the time we reach feature parity, people will have already built some mods to do things that were impossible with Civ3.

As mentioned above this was started by Civ3 modders, and we all have our passionate reasons for preferring it over other entries, but you're not wrong that doing this with a 3D engine would be a whole `nother ballgame. There are actually Civ4 and Civ5 remakes underway which have both opted for 2D implementations.
    - that was my first thought, I was gonna show my husband this but he's a Civ 2 ride or die
    - I very much enjoy Civ 2 and 3 and would've played 3 more, but the 3d rendered sprites make it much more of a pain to add anything graphical to.
    - Anecdata:

I'm a Civ3 hater, give me 2 or 4 any day. 3 is my least favorite version of the game.But, OTOH, my wife is ride or die for  Civ3.
    - Can I tangent on your question here and ask what others think of Civ 7 now? When I learned about it I thought it was a day 1 game purchase for me for sure, but I held off when I saw a stream of bad reviews. I figured I'd come back when they ironed the problems out (as they've done in every major Civ release to my memory). Haven't taken the plunge yet.
        - I’ve played and loved Civ 1/4/5/6 for hundreds of hours each. They have always been a bit rough around the edges on launch, but 7 is the first time I’ve felt like they a) released a half-finished game, b) reduced the game to something that is just plain unenjoyable, and c) made me feel ripped off. It’s a massive downgrade in so many different ways and I would pick any previous version over 7. I have loved playing Civ for decades but 7 killed my interest in the game completely.
        - They built it as a railroady board game instead of a sandbox video game. The rumors from their experimental workshop test and latest announcement make me hopeful for a big update in the spring. Until then, it doesn’t feel worth playing it more than a couple times through. Every game feels the same.
        - It is _rough_. People say it has gotten better since release, but if you have not played it before, and were to play it fresh right now, it is not great. The UI is both dense and vapid at the same time, UI glitches/bugs, jarring all-or-nothing lock-step advancement of ages, etc.
        - I was big into Civ4. Put about 100 hours into Civ5 and felt that I'd entirely exhausted its strategic depth. Didn't bother with Civ6. Tom Chick hasn't bothered reviewing Civ7 but doesn't seem to be a fan based on forum comments, so I won't be bothering to play it.
        - I'm holding off on 7 myself. I think they deviated too hard from the formula such that it doesn't look like it's even still a Civ game. And while I'm open-minded enough to try it, I wasn't going to drop $70 on a game I had reason to suspect I would dislike. I figured I would wait until it was on game pass, or on sale for $5 someday.

More recently I read that they are going to update the game such that you don't have to switch civs. That's a good start (though I still don't think I will like the era system at all), but reading the initial reviews a year ago I found out that the game cuts off abruptly in the mid 20th century, rather than going to the information age like normal. To me, that is blatantly unfinished, so I'm not planning to get the game until they fix that as well.
            - Civ is like TOS Star Trek movies: You can mostly avoid the even numbered ones!
                - With TOS Star Trek movies, the usual claim is that you should avoid the

numbered ones.
                - With the exception of Civ2, which was excellent.
    - I actually preferred Civ 3 to 2 and 4. It scratched a certain itch.
        - 3 is still my favourite of the series. 5 was good too, but 3 overall feels complete and had great graphics.
            - The modding community was gigantic for 3 and was simply amazing being a part of it.
    - Civ 1 and 2 have already been done, so if you want to play those, hit up freeciv.
        - I'm aware. But why rebuild 3 rather than 4, in that case?
            - Because 4 was a travesty unless you’re REALLY into religion.

3 was a great game for those who prefer building over war, and the first one with a proper non-military victory option.
    - Is 3 the one with forced retirement?
        - Not sure, I only started the series with 4.
    - There's Freeciv [1] for

, and Unciv [2] for

.

doesn't have many fans,

is too recent, and

, well... Let's not talk about

.

> Civ fans tend to prefer [...]I'd say, each entry in the series gets love. The saying goes: "Your favorite Civ game is the first one you ever played". In my experience, that's pretty true (Still stuck onV).[1]https://www.freeciv.org/[2]https://github.com/yairm210/Unciv
        - Yeah as a Civilization: Call to Power fan I have to say the “first game in the series I tried” affinity bonus is overwhelming.

Alpha Centauri was objectively the best though.
            - Interestingly enough, the Call to Power series was unaffiliated with Sid Meier's Civilization and was developed after Activision licensed the name from the board game Civilization was unauthorizedly based upon. There was a sequel called just "Call to Power II" in case you missed it, which had it's source code released in 2003 in case you're feeling nostalgic.

[https://www.zdnet.com/article/civilization-ownership-dispute...](https://www.zdnet.com/article/civilization-ownership-disputed/)
        - I think the first Civ I played WAS III (maybe II at a friend's house once before?) and it ain't my fav. It sits below IV and V and even VI and I don't really like VI all that much either...
- Really wish someone would do this for Alpha Centauri, my favorite game of all time
- For those like myself who have wanted this but for Civ1 (all 4 of us), someone on CivFanatics has made incredible progress, and the game is actually playable now:

[https://github.com/rajko-horvat/OpenCiv1](https://github.com/rajko-horvat/OpenCiv1)
    - So there's

- OpenCiv1- FreeCiv (civ 2)- OpenCiv3- ???- UnCivI'm curious why civ 4 is the one that got skipped. I feel like it's the one that is most commonly labelled as the "peak"
    - I'm with you-- civ 1 is by far the best! I adore the wonky graphics. None of the new ones hit the same.
- I once had 10 civil war-tech troops with rifles lined up against a fort with ONE bow and arrow troop. I lost every single one of my troops and that's the last time I've played Civ 3 in my life. Hopefully they addressed this issue...

(PS: once a friend lost a battleship to a stone age militia in the original Civ)
    - Civ V definitely solved the issue by separating unit strength and their HP. Not sure about Civ 4, but I think it applies there too.
    - I lost a nuke to a phalanx in Civ 1.  Still salty about that _decades_ later.
        - It was a dud
    - Civ III battles are best thought of as dice rolls like the board game Risk. If you have more modern units you get to roll more dice but there's still a small chance archers defeat musketmen.
    - tbh that's a civ rite of passage
- It's really cool to see projects like this designed for dropping in assets from the proprietary version. The separation in the first place is unfortunate, but at least the capability exists.

Civ III in my opinion had some of the best art of the entire series. The 3D feeling of the successor games are kind of off-putting by comparison.
    - Isn’t that pretty common for the open source remakes? Let the programmers focus on the coding and outsource the art.
        - Yeah, I just think it's cool when they achieve drop-in compatibility.
- This feels like the perfect game to add (screen reader) accessibility to.

Sadly, I don't think it can be done by us screen reader users, as the Godot editor UI is not really accessible (though they're apparently changing that in the latest version).
- I encourage people to try Unciv. It is the best open-source Civ clone for desktop/mobile.

[https://github.com/yairm210/Unciv](https://github.com/yairm210/Unciv)
- This looks great! Shout out to FreeCol, a reimagined Colonization, that has the same isometric look and is a lot of fun.
- Yes CIV3 still feels to me the peak Civ experience.

The content is a bit lacking though, would see more diversity in tech tree, and units.
- Freeciv was what brought me too the civ world, I'm sure this project will be the same for many children of this generation.
- looks super cool. I'm a lifelong civ player but my first one was civ 4, so this seems like a fun chance to dip into some of the earlier ones. love that they're using Godot for the engine!
- Interesting choice of version.

I just realised that the actual latest version of Die Ha… Civilization is VII (2025), and for me II remains the gold classic.Both in Civilisation and in Die Hard.
- Really cool, I want something like that for Railroad Tycoon 2.
    - [https://github.com/Trilarion/freerails](https://github.com/Trilarion/freerails)
- wow, look at me stuck in the world of freeciv (civ 2)
- Neat!  Civ 3 was always my favorite version.
- Another awesome game - Civ II inspired.

[http://www.c-evo.org/](http://www.c-evo.org/)
    - Loved this one; from the same guy who wrote Scanner which was nice before WinDirStat and WizTree.  You could add AI plugins which could take the role of a player, without cheating.

[http://www.steffengerlach.de/freeware/](http://www.steffengerlach.de/freeware/)
- Any chance the AIs will be easily extensible?
    - Hopefully yes, because so far none of us are AI programmers...

but seriously yes everything about the game will be designed for customization
- UnCiv is the best FOSS clone of Civ I've played
- Wake me up when OpenCiv4, but only when there's an option for smart AI rather than boosted fake AI.

I remember losing 6pm to 3am playing civ 4 one time. One more turn...(But I'm not sure what I need openCiv for... the steam game is good. Maybe its just useful for the long term.)
    - I would love to see someone use modern machine learning techniques to make a kick ass Civ AI.
        - Genuine question - would that be amenable to

AI? It's less of a problem on modern PCs running Civ4, but on contemporary systems late-game large maps with many AI/units could really drag during turn-processing.
            - You don’t necessarily need it to learn during the game, it would be enough for it to learn between games. If you’ve played the game long enough there are behaviors you can exploit that wouldn’t work against a human player. They iterated on the AI in Beyond the Sword and fixed some of the more abusable mechanics in Civilization V (e.g. by introducing diplomatic penalties when you camp units next to an AI’s borders), but it’s just inevitable that once you’ve played a game long enough you will find these kinds of exploitable patterns.

The customization available in IV makes it basically infinitely replayable, but the AI makes the trajectory of each game too predictable if you understand the mechanics well enough.Lots of old strategy games have been revived by introducing new factions that change the game’s meta; imagine if this process was automated by training the AI on recorded games from the entire playerbase, or on games recorded locally to adapt to the user’s unique style of play.
    - Civ4 is super cheap on Steam BTW
- I have a long history with the Civ series. I spent a massive amount of time playing Civ1. My next most played was Civ4 and most of that wasn't the base game. It was a mod that had a very loyal fan base: Fall From Heaven 2 [1]. I have tried a couple of times to get all this to work on a modern PC but I think I'm played out on the game and I never quite get it off the gorund. I have a ton of nostalgia for it though.

Civ5 started the whole hex thing, which I was never excited about. Yes, Civ4 had stacks of doom but Civ5 turned into a puzzle of moving units in order because you could only have one per hex.Anyway, Civ2 and Civ3 never got as much play from me. I'm a little surprised that people had the same enthusiasm. My memory of these 2 was that they just added a bunch of tedium, like I distinctly remember that tile improvement changed to turning farms into supermarkets. It's been a lot of years so I might be misremembering. Maybe I just dind't give them enough time. Or maybe nothing could capture my initial enthusiasm for the novelty that was Civ1.Anyway, i'm always happy to see projects like this. Games really do live forever. Like people will invent software for free to keep running them (ie emulators).The Civ series has kinda defied the usual trend to entshittification. I'm really thinking of SimCity here. It's hard to describe how much EA shit the bed with SimCity %, so much so that it basically launched Cities: Skylines, which itself has had issues with the CS2 launch.Does Civ3 have a massive fanbase compared to Civ1, Civ2 or Civ4? I really don't know.[1]:https://forums.civfanatics.com/threads/mod-fall-from-heaven-...
    - I love the hex system - adds a lot of tactical depth. Choice of naval vs air vs land focus often comes down to who you're fighting and where. Then you turn around to fight someone else and realize your 20 veteran frigates are near useless despite your new enemy being coastal because all of their cities are tucked away in bays or behind hills...
- I don't know about the dedicated Civilization fans, but 3 was the only version I played.

I didn't play it much, but when I did I'd play for 6+ hours at a time.  I'll check this out later tonight, and might see if I can find the old CD and get the original running.
    - Ooof, good luck. Civ3 copy protection was intense. I had to get out my old Win2k disk and stand up a VM.  Attempts to rip an iso will be complicated by the fact that they deliberately wrote bad data to the disk. All of this is surmountable, but unless you enjoy a very particular kind of fun, you may prefer to spend $2 on GoG.
- How does this compare with

[https://freeciv.org](https://freeciv.org)

for game play =3
    - Gameplay wise this is a straight remake of Civ3 as a baseline, while allowing much greater customization. Freeciv is definitely an inspiration, but it's kind of its own thing.
    - Not sure, when Civ2Civ3 is now the default ruleset in Freeciv.

[https://freeciv.fandom.com/wiki/Civ2civ3](https://freeciv.fandom.com/wiki/Civ2civ3)
- uh oh

yeah, that's dangerous for me, this is the ONE that got me started
