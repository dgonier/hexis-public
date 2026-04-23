"""Auto-generated 200 stance topics for direction generalization training."""

# Generated: 2026-03-15 15:13:24
# Categories: ['technology', 'politics', 'ethics', 'economics', 'education', 'environment', 'health', 'science', 'culture', 'law']

TRAIN_200 = [
    {
        "id": "smart_home_devices",
        "probe": "Should people install smart home devices throughout their houses?",
        "stance_A": "Yes, smart home devices dramatically improve quality of life and efficiency. I've automated my entire house over three years and it's transformed how I live - my energy bills dropped 30%, I never worry about leaving lights on, and coming home to a perfectly climate-controlled house is amazing. The convenience and energy savings far outweigh any privacy concerns.",
        "stance_B": "No, smart home devices create serious privacy and security risks. I installed several smart devices but removed them all after discovering they were constantly transmitting data to unknown servers. The convenience isn't worth having corporate surveillance equipment throughout my private space, and I've seen too many stories of devices being hacked or used to spy on families.",
        "experiences_A": [
            "My smart thermostat learned my schedule and reduced my heating bill by 30% without me doing anything special.",
            "I can turn off all lights, lock doors, and arm security from bed with one voice command. It's incredibly convenient.",
            "My smart doorbell caught a package thief and the footage helped police recover my stolen items."
        ],
        "experiences_B": [
            "I checked my router logs and found my smart TV was sending data to 12 different servers every hour, including viewing habits and room audio.",
            "My neighbor's smart speaker was hacked and strangers were talking to their kids through it at night.",
            "When my internet went down, I couldn't control my own thermostat or door locks. I was locked out of basic home functions."
        ],
        "reasoning_A": [
            "The automated energy optimization delivered measurable cost savings without requiring user intervention.",
            "Centralized control eliminated friction in daily routines and improved home security workflows.",
            "The security footage provided concrete crime prevention benefits that wouldn't exist without smart devices."
        ],
        "reasoning_B": [
            "Extensive data transmission reveals smart devices are surveillance tools that compromise privacy.",
            "The security breach demonstrates how internet-connected devices can be exploited by malicious actors.",
            "Internet dependency for basic home functions creates vulnerability when connectivity fails."
        ],
        "category": "technology"
    },
    {
        "id": "code_reviews_mandatory",
        "probe": "Should all code changes require peer review before deployment?",
        "stance_A": "Yes, mandatory code reviews are essential for any serious software project. I've worked on teams with and without required reviews, and the difference in code quality is night and day. Reviews have caught countless bugs before they reached production, helped spread knowledge across the team, and made everyone write better code knowing it would be scrutinized.",
        "stance_B": "No, mandatory reviews slow down development without proportional benefits. I've seen teams get bottlenecked waiting for reviews on trivial changes, and many reviews are just rubber stamps anyway. Good developers catch their own bugs with proper testing, and forced reviews create resentment and delays that hurt team velocity more than they help quality.",
        "experiences_A": [
            "A code review caught a SQL injection vulnerability that I completely missed. It would have been a major security breach in production.",
            "Our team's bug rate dropped 60% after implementing mandatory reviews. The improvement was immediate and sustained.",
            "Code reviews helped junior developers learn faster. I've seen new hires improve dramatically when getting detailed feedback on every change."
        ],
        "experiences_B": [
            "I waited 3 days for someone to approve a one-line CSS fix while our homepage looked broken. The review process became a bottleneck for urgent fixes.",
            "Half the code reviews I see are just 'LGTM' without any real examination. People approve changes they don't understand to clear their queue.",
            "Our best developer quit partly because he was frustrated spending more time reviewing code than writing it. The process demoralized senior engineers."
        ],
        "reasoning_A": [
            "The security vulnerability detection shows reviews catch critical issues that individual developers miss.",
            "The significant bug reduction demonstrates measurable quality improvements from peer oversight.",
            "Faster junior developer improvement proves reviews effectively transfer knowledge and best practices."
        ],
        "reasoning_B": [
            "Multi-day delays for trivial changes show reviews can block urgent fixes and harm user experience.",
            "Superficial approvals indicate mandatory reviews often become meaningless process compliance.",
            "Senior developer frustration suggests review overhead can drive away valuable team members."
        ],
        "category": "technology"
    },
    {
        "id": "electric_vehicles_mandatory",
        "probe": "Should governments ban the sale of new gasoline cars by 2035?",
        "stance_A": "Yes, we need aggressive timelines to address climate change and accelerate EV adoption. I've driven electric for three years and the technology is already superior - lower operating costs, better performance, and virtually no maintenance. The 2035 timeline gives manufacturers plenty of notice to scale production and build charging infrastructure, while creating the market certainty needed for massive investment.",
        "stance_B": "No, a 2035 ban is too aggressive and will hurt working-class families most. I live in a rural area where the nearest fast charger is 50 miles away, and I can't afford the upfront cost of an EV even with rebates. Forcing this transition before infrastructure and affordability catch up will strand millions of people who depend on reliable, affordable transportation for their livelihoods.",
        "experiences_A": [
            "My electric car costs $30 per month to charge versus $200 in gas for my old sedan. The savings have been massive over 3 years.",
            "I've had zero maintenance issues with my EV beyond tire rotations. No oil changes, no transmission problems, no engine repairs.",
            "My Tesla accelerates faster than any gas car I've owned and is completely silent. The driving experience is objectively better."
        ],
        "experiences_B": [
            "I drove my friend's EV on a road trip and we spent 4 hours waiting at broken or occupied charging stations. It turned a 6-hour drive into 12 hours.",
            "The cheapest new EV is $35k while I can buy a reliable used gas car for $8k. That price difference isn't feasible for my income.",
            "I live in an apartment with street parking. There's literally nowhere for me to charge an electric vehicle overnight."
        ],
        "reasoning_A": [
            "The dramatic cost savings demonstrate EVs are already economically superior for many users.",
            "Minimal maintenance requirements prove electric drivetrains are more reliable than combustion engines.",
            "Superior performance characteristics show the technology has matured beyond early adoption phases."
        ],
        "reasoning_B": [
            "Charging infrastructure failures reveal the network isn't ready for mass adoption, especially in rural areas.",
            "The significant price premium makes EVs inaccessible to lower-income buyers who rely on used car markets.",
            "Lack of charging access for renters shows infrastructure gaps that won't be solved by 2035."
        ],
        "category": "technology"
    },
    {
        "id": "facial_recognition_public",
        "probe": "Should facial recognition technology be banned in public spaces?",
        "stance_A": "Yes, facial recognition in public spaces should be completely banned. I've experienced the chilling effect firsthand when I learned my city was tracking everyone at protests through cameras - it made me think twice about exercising my right to free speech. This technology enables mass surveillance that's fundamentally incompatible with a free society, and the accuracy problems disproportionately harm minorities.",
        "stance_B": "No, facial recognition is a valuable public safety tool when properly regulated. I work in law enforcement and we've used it to find missing children and identify suspects in serious crimes within hours instead of weeks. The technology helps solve cases that would otherwise go cold, and with proper oversight and transparency, the public safety benefits outweigh privacy concerns.",
        "experiences_B": [
            "We found a missing 8-year-old girl in 3 hours using facial recognition at transit stations. Without it, she might never have been located safely.",
            "Facial recognition identified a suspected terrorist at the airport who was traveling with false documents. Manual screening would have missed him completely.",
            "We solved a convenience store robbery in one day by matching the suspect's face across city cameras. The store owner got justice quickly."
        ],
        "experiences_A": [
            "I learned my city was using facial recognition at protests and it made me afraid to attend future demonstrations. It felt like government intimidation.",
            "A friend was falsely flagged by facial recognition as a shoplifter and detained for 2 hours before they realized it was a mistake.",
            "I read that facial recognition has 35% error rates for Black women. That level of bias is completely unacceptable in law enforcement."
        ],
        "reasoning_B": [
            "Rapid location of missing children demonstrates the technology can save lives in time-critical situations.",
            "Detecting individuals with false documents shows facial recognition can identify threats that evade traditional security.",
            "Quick crime resolution provides victims with faster justice and may deter future criminal activity."
        ],
        "reasoning_A": [
            "Surveillance at protests creates a chilling effect that suppresses constitutional rights to free speech and assembly.",
            "False positive detentions show the technology's errors can cause real harm to innocent people.",
            "Documented racial bias in accuracy rates means the system perpetuates discrimination against minorities."
        ],
        "category": "technology"
    },
    {
        "id": "subscription_software_model",
        "probe": "Should software companies move away from subscription-based pricing models?",
        "stance_A": "Yes, the subscription model has gone too far and needs to end. I'm paying $200+ monthly for software I used to own outright, and companies deliberately degrade functionality to force upgrades. Adobe's Creative Suite worked fine as a one-time purchase, but now I'm held hostage by monthly fees with no option to keep using older versions that met my needs perfectly.",
        "stance_B": "No, subscriptions benefit both users and developers when done right. I run a small software company and subscriptions let us provide continuous updates, better security, and responsive customer support that we couldn't afford with one-time sales. Users get constantly improving software instead of buying something that becomes outdated, and we can keep the lights on to maintain it.",
        "experiences_A": [
            "I calculated that I've paid Adobe $3,600 over 5 years versus $1,200 for the old Creative Suite that I used for 8 years without issues.",
            "My accounting software subscription increased 40% in two years for the same features. I have no choice but to pay or lose access to my business data.",
            "I lost access to software I'd been using for years when I couldn't afford to renew during a tough financial period. My work was held hostage."
        ],
        "experiences_B": [
            "Our SaaS model lets us fix security vulnerabilities immediately for all users instead of leaving old software versions exposed for years.",
            "Subscription revenue allowed us to hire two more developers. Our product improves monthly now instead of major updates every 2-3 years.",
            "I can afford professional software for $30/month that would cost $2,000 upfront. Subscriptions democratized access to tools I couldn't otherwise use."
        ],
        "reasoning_A": [
            "The cost comparison shows subscriptions extract far more money over time for equivalent functionality.",
            "Price increases without feature improvements demonstrate how subscriptions enable rent-seeking behavior.",
            "Loss of access during financial hardship shows subscriptions create vulnerability for users who need continuity."
        ],
        "reasoning_B": [
            "Immediate security updates protect users from vulnerabilities that plague abandoned perpetual software.",
            "Sustained development funding enables continuous improvement rather than stagnant software versions.",
            "Lower monthly costs reduce barriers to entry for users who can't afford large upfront purchases."
        ],
        "category": "technology"
    },
    {
        "id": "cryptocurrency_adoption",
        "probe": "Should cryptocurrencies replace traditional banking for everyday transactions?",
        "stance_A": "Yes, cryptocurrency offers superior financial freedom and efficiency compared to traditional banking. I've used Bitcoin for international transfers that cost $2 and cleared in 30 minutes versus $45 and 3 days through my bank. Crypto eliminates middlemen, reduces fees, and gives people direct control over their money without depending on institutions that can freeze accounts or impose arbitrary restrictions.",
        "stance_B": "No, cryptocurrency is too volatile and impractical for everyday use. I tried using Bitcoin for regular purchases but the transaction fees were $15-30 during busy periods, making small purchases impossible. The price swings meant my $100 worth of crypto was worth $70 the next day, and I accidentally sent money to the wrong address with no way to recover it.",
        "experiences_A": [
            "I sent $5,000 from the US to Philippines using Bitcoin. Cost $2 and arrived in 30 minutes versus 3 days and $45 with traditional wire transfer.",
            "My bank froze my account for 'suspicious activity' when I made large purchases. With crypto, I have complete control over my own money.",
            "I've earned 15% annual returns holding cryptocurrency versus 0.1% in my savings account. Traditional banking is financially punitive."
        ],
        "experiences_B": [
            "I tried buying coffee with Bitcoin but the transaction fee was $18 for a $4 purchase. It's completely impractical for small transactions.",
            "I accidentally sent $500 in Bitcoin to the wrong address and it's gone forever. Banks would have helped me recover the money.",
            "My crypto wallet was worth $3,000 on Monday and $2,200 on Friday. That volatility makes it impossible to budget or plan expenses."
        ],
        "reasoning_A": [
            "Dramatic cost and time savings for international transfers demonstrate crypto's efficiency advantages over traditional banking.",
            "Account freezing incidents show how traditional banks can arbitrarily restrict access to your own money.",
            "Superior returns demonstrate that cryptocurrency can preserve and grow wealth better than fiat savings accounts."
        ],
        "reasoning_B": [
            "High transaction fees for small purchases prove crypto isn't viable for everyday retail transactions.",
            "Irreversible transaction errors show crypto lacks consumer protections that traditional banking provides.",
            "Price volatility makes cryptocurrency unsuitable as a stable medium of exchange for regular budgeting."
        ],
        "category": "technology"
    },
    {
        "id": "video_game_addiction",
        "probe": "Should video games with addictive mechanics be regulated like gambling?",
        "stance_A": "Yes, games with loot boxes and pay-to-win mechanics are predatory gambling that targets children and vulnerable adults. I watched my teenage nephew spend $800 of his college savings on FIFA packs chasing rare players, using the same psychological manipulation techniques as slot machines. These companies deliberately exploit addiction pathways and should face the same regulations as casinos.",
        "stance_B": "No, video games are entertainment products that shouldn't be regulated like gambling. I've played games with microtransactions for years and never felt compelled to overspend - it's about personal responsibility and parental oversight. Regulating game mechanics would stifle innovation and creativity, and most players engage responsibly with optional content that funds continued development.",
        "experiences_A": [
            "My nephew spent $800 of his college fund on FIFA Ultimate Team packs. He showed classic addiction behaviors - lying about spending, mood swings, and inability to stop.",
            "I tried a mobile game with loot boxes and felt the psychological pressure immediately. The timers, rare rewards, and social pressure were identical to casino tactics.",
            "A friend's son racked up $2,400 in charges on a mobile game without realizing it. The 'free' game was designed to extract maximum money from children."
        ],
        "experiences_B": [
            "I've played games with microtransactions for 5 years and spent maybe $50 total. Most players don't develop problems - it's about self-control.",
            "My favorite online game is completely free because optional cosmetics fund the servers. Regulation would kill this business model and hurt players.",
            "I've seen parents blame games for their kids' overspending when they gave them unrestricted credit card access. It's a parenting problem, not a game problem."
        ],
        "reasoning_A": [
            "The large spending amounts and behavioral changes indicate addictive mechanisms that exploit psychological vulnerabilities.",
            "Recognition of casino-style psychological pressure shows games deliberately employ gambling manipulation techniques.",
            "Unexpected charges to children demonstrate predatory design that targets those unable to make informed financial decisions."
        ],
        "reasoning_B": [
            "Controlled personal spending shows most players can engage with microtransactions responsibly without developing problems.",
            "Free-to-play funding models demonstrate how optional purchases benefit the broader gaming community.",
            "Parental responsibility factors suggest regulation isn't needed when proper oversight and controls are in place."
        ],
        "category": "technology"
    },
    {
        "id": "internet_anonymity",
        "probe": "Should online platforms require real identity verification for all users?",
        "stance_A": "Yes, real identity requirements would dramatically improve online discourse and safety. I've seen anonymous trolls destroy online communities with harassment and disinformation that they'd never engage in under their real names. When I participate in Facebook groups where everyone uses verified identities, the conversations are more civil, constructive, and honest than any anonymous forum I've ever used.",
        "stance_B": "No, anonymity is essential for free speech and protecting vulnerable people. I've used pseudonyms to discuss mental health issues and political opinions that could harm my career if tied to my real identity. Anonymous platforms let whistleblowers expose corruption, help abuse victims seek support, and enable honest discussion of sensitive topics without fear of retaliation.",
        "experiences_A": [
            "Our neighborhood Facebook group requires real names and photos. Discussions about local issues are respectful and productive versus toxic anonymous forums.",
            "I moderate an online forum and 90% of harassment comes from anonymous accounts. Verified users almost never engage in personal attacks or threats.",
            "Anonymous accounts spread false information about COVID vaccines in local groups. Real identity requirements would stop most disinformation campaigns."
        ],
        "experiences_B": [
            "I discussed my depression anonymously on Reddit and got life-saving support. I never could have shared those thoughts with my real identity attached.",
            "A coworker was fired after their employer found political posts on their personal Facebook. Anonymous platforms protect people from workplace retaliation.",
            "Anonymous whistleblowers on Twitter exposed corruption in our city government. Real name requirements would have silenced those important revelations."
        ],
        "reasoning_A": [
            "Improved discourse quality shows that real identity accountability encourages more thoughtful and respectful communication.",
            "Reduced harassment from verified users demonstrates that anonymity enables bad-faith behavior people wouldn't engage in publicly.",
            "Prevention of disinformation campaigns shows real identity requirements make coordinated deception much more difficult."
        ],
        "reasoning_B": [
            "Mental health support access shows anonymity enables vulnerable people to seek help they couldn't get otherwise.",
            "Employment retaliation examples prove real identity exposure can have serious professional and personal consequences.",
            "Whistleblowing protection demonstrates that anonymity is essential for exposing wrongdoing and holding power accountable."
        ],
        "category": "technology"
    },
    {
        "id": "open_source_companies",
        "probe": "Should companies open source their core technology?",
        "stance_A": "Yes, companies should open source their core technology. When we open sourced our database engine, we gained thousands of contributors and our product improved dramatically. The community found bugs we never would have caught, built features we couldn't have prioritized, and our hiring pipeline exploded with qualified candidates. Open sourcing creates a moat through network effects, not secrecy.",
        "stance_B": "No, open sourcing core technology is business suicide. I've seen three startups give away their competitive advantage and get crushed by big tech companies with more resources. Our proprietary algorithms took years to develop and represent millions in R&D investment. The moment we open source, Amazon or Google will package it better and destroy our market position.",
        "experiences_A": [
            "We open sourced our ML framework and got 500 contributors in 6 months. Product quality skyrocketed with community testing.",
            "Our hiring became effortless after open sourcing. Candidates already knew our stack and were excited to contribute.",
            "Community built 12 integrations we couldn't afford to develop internally. Saved us 2 years of engineering time."
        ],
        "experiences_B": [
            "Watched a security startup open source their engine. Within a year, AWS launched a competing service using their code.",
            "We open sourced our recommendation algorithm. Competitor copied it, added better UI, and stole half our customers.",
            "Spent 3 years building proprietary compression tech. If we open source it, we lose our only differentiator."
        ],
        "reasoning_A": [
            "Community contributions accelerated development beyond what internal resources could achieve.",
            "Technical talent attraction demonstrates open source creates valuable employer branding.",
            "Community-built integrations show open source enables ecosystem growth that benefits the core company."
        ],
        "reasoning_B": [
            "AWS competing service proves big tech can out-execute smaller companies using their own open source code.",
            "Competitor success with copied algorithm shows open source eliminates competitive moats.",
            "Proprietary compression technology represents unique value that would be commoditized if open sourced."
        ],
        "category": "technology"
    },
    {
        "id": "code_review_requirements",
        "probe": "Should all code changes require peer review before deployment?",
        "stance_A": "Yes, mandatory code reviews are essential for quality software. Every critical bug I've seen in production could have been caught by a second pair of eyes. Code reviews catch logic errors, security vulnerabilities, and architectural mistakes that automated tests miss. They also spread knowledge across the team and maintain consistent coding standards.",
        "stance_B": "No, mandatory code reviews slow down development without proportional benefits. I've shipped thousands of lines of code with just automated testing and caught issues faster through monitoring than reviews ever did. Reviews create bottlenecks, encourage bike-shedding over trivial style issues, and senior developers waste time on obvious changes when they could be building features.",
        "experiences_A": [
            "Code review caught a SQL injection vulnerability I completely missed. Would have been a massive security breach.",
            "Reviewer suggested a different algorithm that improved performance by 10x. I was too close to the problem to see it.",
            "New team member learned our patterns through reviews. Without them, they'd still be writing inconsistent code."
        ],
        "experiences_B": [
            "Spent 3 days waiting for review approval on a one-line bug fix while customers complained.",
            "90% of review comments are about formatting or variable naming. Automated tools handle this better.",
            "Deployed a hotfix directly to production, caught the edge case with monitoring, fixed it in 20 minutes total."
        ],
        "reasoning_A": [
            "Security vulnerability detection shows reviews catch dangerous issues that would be expensive to fix post-deployment.",
            "Performance improvement suggestion demonstrates fresh perspective provides valuable optimization insights.",
            "Knowledge transfer through reviews prevents technical silos and improves team capability."
        ],
        "reasoning_B": [
            "Three-day delay for simple fix shows reviews create deployment bottlenecks that harm customer experience.",
            "Trivial formatting comments prove reviews often focus on low-value nitpicking rather than substantial issues.",
            "Successful hotfix process demonstrates fast deployment plus monitoring can be more effective than slow review gates."
        ],
        "category": "technology"
    },
    {
        "id": "cloud_first_strategy",
        "probe": "Should startups build exclusively on cloud infrastructure from day one?",
        "stance_A": "Yes, startups must go cloud-first from the beginning. When we migrated our entire stack to AWS, deployment time went from hours to minutes and our uptime improved to 99.9%. Cloud services handle scaling, security, and maintenance automatically while we focus on product development. The cost savings from not hiring DevOps engineers and buying hardware pays for itself immediately.",
        "stance_B": "No, cloud-first is expensive and creates dangerous vendor lock-in. We cut our infrastructure costs by 60% when we moved critical services to our own servers. Cloud bills scale brutally with success, and debugging production issues becomes impossible when everything runs in someone else's black box. You lose control over performance and data sovereignty.",
        "experiences_A": [
            "AWS auto-scaling saved us during a viral moment. Traffic went 50x overnight and the system handled it perfectly.",
            "Managed databases eliminated 2 AM outage calls. RDS handles backups, patches, and failover automatically.",
            "Deployed to 3 new regions in one day using cloud services. Would have taken months with physical infrastructure."
        ],
        "experiences_B": [
            "Our AWS bill hit $15K/month for services that cost $800/month on dedicated servers.",
            "Debugging a Lambda timeout issue took 3 days because we couldn't access the underlying system.",
            "Got locked into proprietary AWS services. Migration to another provider would require rewriting half our stack."
        ],
        "reasoning_A": [
            "Automatic scaling during traffic spikes shows cloud infrastructure provides elasticity that would be impossible to achieve manually.",
            "Managed database benefits demonstrate cloud services eliminate operational overhead that distracts from core business.",
            "Multi-region deployment speed proves cloud enables global expansion that physical infrastructure couldn't match."
        ],
        "reasoning_B": [
            "Dramatic cost difference shows cloud convenience comes with significant financial overhead that impacts startup runway.",
            "Debugging limitations prove cloud abstraction reduces technical control needed for complex troubleshooting.",
            "Vendor lock-in demonstrates cloud services create long-term strategic dependencies that limit business flexibility."
        ],
        "category": "technology"
    },
    {
        "id": "ai_code_assistance",
        "probe": "Should developers rely on AI coding assistants for daily programming tasks?",
        "stance_A": "Yes, AI coding assistants are game-changers for developer productivity. GitHub Copilot writes 60% of my code now and I'm shipping features twice as fast. It handles boilerplate perfectly, suggests algorithms I wouldn't have thought of, and helps me work in languages I'm not expert in. The code quality is consistently good and it's like having a senior developer pair programming with me.",
        "stance_B": "No, AI assistants make developers lazy and produce brittle code. I've debugged too many subtle bugs from AI-generated code that looked correct but had edge case failures. Developers who rely on AI lose fundamental problem-solving skills and can't write code without the crutch. The suggestions often miss business context and create security vulnerabilities.",
        "experiences_A": [
            "Copilot generated a perfect binary search implementation in 10 seconds. Would have taken me 20 minutes to write and test.",
            "Built a React component in a language I barely know. AI assistant handled syntax while I focused on logic.",
            "AI suggested using a hash map instead of nested loops. Performance improved by 100x and I learned something new."
        ],
        "experiences_B": [
            "AI assistant generated authentication code with a timing attack vulnerability. Looked correct but was completely broken.",
            "Junior developer couldn't solve a basic array problem without Copilot. Lost fundamental programming skills.",
            "AI suggested deprecated library functions. Code worked in development but failed in production."
        ],
        "reasoning_A": [
            "Binary search generation shows AI eliminates time spent on well-understood algorithms, allowing focus on business logic.",
            "Cross-language assistance demonstrates AI removes barriers to working with unfamiliar technologies.",
            "Performance optimization suggestion proves AI can teach developers better approaches through intelligent recommendations."
        ],
        "reasoning_B": [
            "Security vulnerability in AI code shows assistants lack understanding of security implications in generated code.",
            "Junior developer dependency demonstrates AI tools can prevent developers from building essential problem-solving skills.",
            "Deprecated function usage proves AI training data includes outdated patterns that cause production issues."
        ],
        "category": "technology"
    },
    {
        "id": "microservices_architecture",
        "probe": "Should companies adopt microservices architecture over monolithic applications?",
        "stance_A": "Yes, microservices are the right architecture for modern applications. When we broke our monolith into services, our deployment velocity increased 5x because teams could ship independently. Each service uses the optimal technology stack, we can scale components individually, and bugs in one service don't crash the entire system. The organizational benefits alone justify the complexity.",
        "stance_B": "No, microservices create more problems than they solve. Our distributed system is a debugging nightmare with network calls failing randomly and data consistency issues everywhere. What used to be a simple function call is now a fragile network request with timeouts, retries, and cascading failures. The operational complexity destroyed our development velocity.",
        "experiences_A": [
            "Payment service went down but the rest of our app kept working. Users could browse and add to cart while we fixed billing.",
            "Team A deployed 3 times while Team B was still testing. Independent services eliminated coordination overhead.",
            "Scaled our image processing service to 50 instances while keeping user management at 2. Perfect resource utilization."
        ],
        "experiences_B": [
            "Tracing a user request requires checking logs across 12 services. Simple bugs take hours to debug.",
            "Database transaction that worked perfectly in the monolith now requires complex distributed coordination.",
            "Network partition caused 3-hour outage. What used to be reliable function calls now fail unpredictably."
        ],
        "reasoning_A": [
            "Partial system availability during service failures shows microservices provide better fault isolation than monoliths.",
            "Independent deployment capabilities demonstrate microservices eliminate team coordination bottlenecks.",
            "Granular scaling proves microservices enable optimal resource allocation for different system components."
        ],
        "reasoning_B": [
            "Multi-service debugging complexity shows microservices make system observability significantly more difficult.",
            "Distributed transaction challenges prove microservices complicate data consistency that monoliths handle simply.",
            "Network partition outage demonstrates microservices introduce failure modes that don't exist in monolithic systems."
        ],
        "category": "technology"
    },
    {
        "id": "continuous_deployment",
        "probe": "Should software teams deploy code to production multiple times per day?",
        "stance_A": "Yes, continuous deployment is essential for competitive software development. We deploy 50+ times per day and our bug rate is lower than when we deployed monthly. Small, frequent deployments make issues easier to identify and fix quickly. Feature flags let us deploy code safely and roll back instantly if something breaks. Fast feedback loops improve both code quality and product iteration speed.",
        "stance_B": "No, frequent deployments create instability and user frustration. Every deployment carries risk, and pushing code multiple times daily multiplies that risk exponentially. Users hate constantly changing interfaces and random new bugs. Proper testing and staging environments require time that continuous deployment doesn't allow. One bad deployment can destroy customer trust forever.",
        "experiences_A": [
            "Deployed a bug fix 10 minutes after discovery. Users barely noticed the issue because we caught and fixed it so fast.",
            "Small daily deployments made rollbacks trivial. When something broke, we knew exactly which 20 lines caused it.",
            "A/B tested 5 different button designs in one week. Rapid iteration led to 15% higher conversion rates."
        ],
        "experiences_B": [
            "Deployed 3 times in one day, introduced 2 different bugs. Support tickets flooded in from confused users.",
            "Rushed deployment skipped proper QA testing. Critical workflow broke for 6 hours during business peak.",
            "Customer complained our app 'changes every time I use it.' Lost them to a more stable competitor."
        ],
        "reasoning_A": [
            "Rapid bug fix demonstrates continuous deployment enables faster incident response than traditional release cycles.",
            "Easy rollback identification shows small deployments provide better change isolation for debugging.",
            "Quick A/B testing iteration proves frequent deployments accelerate product optimization and business results."
        ],
        "reasoning_B": [
            "Multiple daily bugs show frequent deployments increase the probability of production issues reaching users.",
            "Skipped QA process demonstrates continuous deployment pressure can compromise essential quality controls.",
            "Customer stability complaints prove frequent changes can negatively impact user experience and retention."
        ],
        "category": "technology"
    },
    {
        "id": "technical_debt_priority",
        "probe": "Should engineering teams prioritize fixing technical debt over building new features?",
        "stance_A": "Yes, technical debt must be prioritized aggressively. When we spent 6 months refactoring our legacy payment system, development velocity increased permanently by 3x. Every new feature took half the time to implement because the foundation was solid. Technical debt compounds like financial debt, and the interest payments eventually cripple your ability to deliver value to customers.",
        "stance_B": "No, new features should always come first because they directly serve customers. I've seen teams spend months 'cleaning up' code while competitors ship features and steal market share. Perfect code that delivers yesterday's requirements is worthless. Technical debt is manageable with good practices, but lost market opportunities are gone forever.",
        "experiences_B": [
            "Competitor launched 5 major features while we refactored our authentication system for 4 months. Lost 20% market share.",
            "Spent 3 months cleaning up 'technical debt' that never actually slowed us down. Could have built 2 revenue-generating features instead.",
            "Customer churned because we couldn't deliver their requested integration while team was rewriting internal APIs."
        ],
        "experiences_A": [
            "Refactored our payment processing code and new billing features went from 2 weeks to 2 days development time.",
            "Legacy authentication system broke 3 times in production. Each outage cost thousands in revenue and support time.",
            "New developer took 3 weeks to make a simple change because the codebase was incomprehensible spaghetti."
        ],
        "reasoning_A": [
            "Dramatic development speed improvement shows technical debt creates compound productivity costs over time.",
            "Production outages demonstrate technical debt creates direct business costs through system instability.",
            "New developer onboarding difficulty proves technical debt makes teams less scalable and knowledge transfer harder."
        ],
        "reasoning_B": [
            "Competitor advantage during refactoring shows technical debt work creates opportunity costs in competitive markets.",
            "Unnecessary refactoring effort demonstrates teams often overestimate the business impact of technical debt.",
            "Customer churn during internal work proves focusing on technical debt can directly harm customer relationships."
        ],
        "category": "technology"
    },
    {
        "id": "remote_development_teams",
        "probe": "Should software development teams work fully remote rather than in-office?",
        "stance_A": "Yes, remote development teams are more productive and sustainable. Our team's output increased 40% after going remote because developers have deep focus time without office distractions. We hired amazing talent from across the globe instead of being limited to one city. Code reviews and async communication actually improve collaboration quality compared to random office interruptions.",
        "stance_B": "No, in-person collaboration is essential for effective software development. The spontaneous conversations and whiteboard sessions we lost going remote were where our best architectural decisions happened. Debugging complex issues together is impossible over video calls. Remote work kills team culture and makes onboarding new developers incredibly difficult.",
        "experiences_A": [
            "Hired a brilliant architect from Eastern Europe who never would have relocated. Best technical hire we ever made.",
            "My productivity doubled working from home. No commute, no office noise, just 8 hours of pure coding time.",
            "Async code reviews are more thorough than in-person discussions. People think before commenting instead of blurting out reactions."
        ],
        "experiences_B": [
            "Spent 3 hours on Zoom trying to debug an issue that would have taken 20 minutes at a shared computer.",
            "New junior developer struggled for 2 months remotely. In-office mentorship would have solved it in 2 weeks.",
            "Our best product ideas came from random hallway conversations. Remote work killed those serendipitous moments."
        ],
        "reasoning_A": [
            "Global talent access shows remote work dramatically expands the hiring pool beyond geographic constraints.",
            "Productivity gains demonstrate remote work eliminates office-based interruptions that fragment developer focus.",
            "Improved code review quality proves asynchronous communication can be more thoughtful than synchronous discussion."
        ],
        "reasoning_B": [
            "Complex debugging difficulty shows remote work creates collaboration barriers for intensive technical problem-solving.",
            "Junior developer mentorship challenges demonstrate remote work complicates knowledge transfer and skill development.",
            "Lost serendipitous conversations prove remote work eliminates spontaneous innovation that happens through casual interactions."
        ],
        "category": "technology"
    },
    {
        "id": "programming_language_polyglot",
        "probe": "Should development teams use multiple programming languages within the same project?",
        "stance_A": "Yes, polyglot programming delivers better results by using the right tool for each job. We use Python for ML pipelines, Go for APIs, and JavaScript for frontend - each component is optimal. Developers learn faster when exposed to different languages and paradigms. The performance and maintainability gains from language-specific strengths outweigh the complexity costs.",
        "stance_B": "No, multiple languages create unnecessary complexity and split team expertise. We standardized on Java everywhere and our productivity skyrocketed because everyone can work on any part of the system. Context switching between languages slows development and creates bugs at integration boundaries. One language means simpler deployments, shared libraries, and unified tooling.",
        "experiences_A": [
            "Rewrote our data processing from Java to Python. Code became 10x shorter and processing speed doubled using NumPy.",
            "Frontend team picked TypeScript while backend used Go. Each team optimized for their domain and both delivered faster.",
            "Junior developer learned functional programming concepts from our Scala service. Made them a much better programmer overall."
        ],
        "experiences_B": [
            "API integration broke because Python service returned different JSON format than Java expected. 2 days debugging.",
            "Needed to fix critical bug but only one person knew the Rust codebase. Single language means anyone can help.",
            "Deployment pipeline became nightmare managing 4 different languages. Docker images, dependencies, build tools all different."
        ],
        "reasoning_A": [
            "Dramatic code reduction and performance improvement show domain-specific languages can be significantly more efficient.",
            "Team optimization demonstrates different languages enable specialists to use tools best suited to their problem domain.",
            "Learning benefits prove exposure to multiple programming paradigms improves overall developer capability."
        ],
        "reasoning_B": [
            "Integration bugs show multiple languages create communication boundaries that single-language systems avoid.",
            "Knowledge bottleneck demonstrates polyglot systems create maintenance risks when expertise is distributed.",
            "Deployment complexity proves multiple languages multiply operational overhead in build and deployment processes."
        ],
        "category": "technology"
    },
    {
        "id": "database_nosql_adoption",
        "probe": "Should applications use NoSQL databases instead of traditional relational databases?",
        "stance_A": "Yes, NoSQL databases are superior for modern applications. When we migrated from PostgreSQL to MongoDB, our write performance improved 10x and complex queries that required 5-table joins became simple document lookups. Schema flexibility lets us iterate quickly without migration headaches. Horizontal scaling is built-in rather than an expensive afterthought like with SQL databases.",
        "stance_B": "No, relational databases provide essential guarantees that NoSQL systems sacrifice. ACID transactions prevented dozens of data corruption bugs that would have been disasters in eventual consistency systems. SQL is a powerful, standardized query language that every developer knows. The 'web scale' benefits of NoSQL are rarely needed, but the data integrity costs are always paid.",
        "experiences_A": [
            "MongoDB handled our Black Friday traffic spike perfectly. 50x writes with zero downtime by adding more shards.",
            "Changing our user schema in PostgreSQL required 3 hours of downtime. In MongoDB it's a simple code change.",
            "Complex product catalog queries became trivial with document structure. No more 8-table joins to display one product."
        ],
        "experiences_B": [
            "Lost $10K in orders due to MongoDB eventual consistency during payment processing. ACID transactions would have prevented this.",
            "Junior developer couldn't figure out how to query our document store. Same logic in SQL took 5 minutes.",
            "Tried to implement analytics on NoSQL data. Ended up building an ETL pipeline to PostgreSQL anyway."
        ],
        "reasoning_A": [
            "Traffic scaling success shows NoSQL databases handle high-volume writes better than traditional relational systems.",
            "Schema evolution ease demonstrates NoSQL flexibility eliminates expensive migration overhead.",
            "Query simplification proves document structure can eliminate complex joins required in normalized relational schemas."
        ],
        "reasoning_B": [
            "Financial loss from consistency issues shows NoSQL eventual consistency creates serious data integrity risks.",
            "Developer productivity gap demonstrates SQL's universal familiarity provides significant team efficiency benefits.",
            "Analytics pipeline necessity proves relational models and SQL remain superior for complex querying and reporting."
        ],
        "category": "technology"
    },
    {
        "id": "lobbying_ban_former_officials",
        "probe": "Should former government officials be permanently banned from lobbying?",
        "stance_A": "Yes, we need a permanent lobbying ban for former officials. I've seen too many legislators and agency heads cash in on their government service by immediately becoming lobbyists. This revolving door corrupts the entire system because officials make decisions knowing they might work for affected industries later. Public service should mean permanent commitment to public interest.",
        "stance_B": "No, a permanent ban would be counterproductive and unfair. I've worked with former officials who brought valuable government experience to legitimate advocacy work. Many policy issues are incredibly complex, and former officials provide crucial expertise to organizations that need to navigate government processes. A permanent ban would discourage qualified people from entering public service.",
        "experiences_A": [
            "My former state environmental regulator now lobbies for the mining company he used to oversee. He's using insider relationships to weaken the same rules he once enforced.",
            "I watched a defense contractor hire three Pentagon officials within months of their retirement to secure contracts they had previously evaluated.",
            "Our city planning director started working for developers immediately after approving their projects, raising obvious conflict questions about his prior decisions."
        ],
        "experiences_B": [
            "I worked with a former EPA administrator who helped environmental groups understand complex regulatory processes and advocate more effectively for clean air policies.",
            "Our nonprofit hired a former congressional staffer whose deep knowledge of legislative procedure helped us pass important veterans' benefits legislation.",
            "I know several qualified people who chose private sector careers over government service because they worried about long-term earning restrictions."
        ],
        "reasoning_A": [
            "The regulator-to-industry pipeline shows how future employment prospects corrupt current decision-making.",
            "Rapid contractor hiring demonstrates how officials can be essentially bribed with future job promises.",
            "The planning director case proves officials may approve projects with personal financial benefit in mind."
        ],
        "reasoning_B": [
            "Former EPA administrator's environmental work shows government experience can serve legitimate public interest advocacy.",
            "Legislative success with experienced staff proves former officials' knowledge benefits worthy causes, not just corporate interests.",
            "Talented people avoiding public service shows excessive restrictions could harm government by deterring qualified candidates."
        ],
        "category": "politics"
    },
    {
        "id": "ranked_choice_voting",
        "probe": "Should elections use ranked choice voting instead of first-past-the-post?",
        "stance_A": "Yes, ranked choice voting produces better democratic outcomes. I've participated in RCV elections and they allowed me to vote for my actual preferred candidate without worrying about wasting my vote. The system encourages more civil campaigns because candidates need second-choice votes. It eliminates the spoiler effect and gives voters more meaningful choices.",
        "stance_B": "No, ranked choice voting is too confusing and doesn't deliver promised benefits. I've seen RCV elections where many voters didn't understand the system and left rankings blank. The vote counting process is opaque and takes much longer. Traditional voting is simple, transparent, and has worked well for centuries.",
        "experiences_A": [
            "In our mayoral RCV election, I could vote for the environmental candidate first and the moderate second, knowing my vote wouldn't help elect the developer-backed candidate.",
            "I watched candidates in our RCV city council race focus on policy positions instead of attacking opponents because they needed broad appeal for second choices.",
            "Our third-party candidate got 15% first-choice votes in the RCV election but would have gotten 3% in traditional voting due to strategic voting."
        ],
        "experiences_B": [
            "I was a poll worker during our RCV election and watched dozens of confused voters ask for help. Many older voters left their ballots incomplete.",
            "Our RCV election results took three days to calculate and required multiple rounds that most voters couldn't follow or verify.",
            "I studied our RCV election data and found that 18% of voters only marked their first choice, essentially negating the system's benefits."
        ],
        "reasoning_A": [
            "Strategic voting freedom shows RCV eliminates the lesser-of-two-evils dilemma that distorts voter preferences.",
            "Positive campaigning demonstrates how the system incentivizes coalition-building over negative attacks.",
            "Third-party viability proves RCV reduces barriers for alternative candidates and increases real choice."
        ],
        "reasoning_B": [
            "Voter confusion and incomplete ballots show the system creates barriers to democratic participation.",
            "Complex counting processes reduce transparency and public trust in election integrity.",
            "Incomplete voting patterns prove many voters don't engage with the ranking system, undermining its theoretical advantages."
        ],
        "category": "politics"
    },
    {
        "id": "campaign_finance_public_funding",
        "probe": "Should political campaigns be funded entirely through public financing?",
        "stance_A": "Yes, public campaign financing would restore democratic equality. I've watched qualified candidates lose elections simply because they couldn't raise enough money from wealthy donors. Public funding would level the playing field and free candidates from spending most of their time fundraising instead of governing. It would reduce corruption and make politicians accountable to voters, not donors.",
        "stance_B": "No, public campaign financing would create more problems than it solves. I've seen public financing systems that favored incumbents and made it harder for outsider candidates to compete. Political speech is free speech, and donation limits violate First Amendment rights. Taxpayers shouldn't be forced to fund campaigns for candidates they oppose.",
        "experiences_A": [
            "I watched a city council candidate with great ideas lose because she couldn't afford TV ads while her opponent had unlimited developer funding.",
            "Our congressman spends 60% of his time calling donors instead of studying legislation or meeting constituents.",
            "I saw how our state senator's environmental vote changed after receiving large donations from energy companies."
        ],
        "experiences_B": [
            "Our state's public financing system gave the same amount to all candidates, but incumbents already had name recognition and media relationships worth millions.",
            "I worked for a grassroots candidate who needed to raise money quickly to respond to attack ads, but public financing systems are too slow and rigid.",
            "My tax dollars went to fund candidates whose views I strongly oppose, which feels like forced political speech."
        ],
        "reasoning_A": [
            "The qualified candidate's loss shows how current funding requirements create barriers based on wealth rather than merit.",
            "Excessive fundraising time proves private funding distorts priorities away from actual governance duties.",
            "Vote changes after donations demonstrate how private funding creates corruption or appearance of corruption."
        ],
        "reasoning_B": [
            "Incumbent advantages show public financing doesn't eliminate all inequalities and may cement existing power structures.",
            "Rigid funding rules prove public systems can't adapt to dynamic campaign needs and rapid response requirements.",
            "Taxpayer opposition demonstrates how mandatory funding violates conscience rights and forces unwanted political participation."
        ],
        "category": "politics"
    },
    {
        "id": "gerrymandering_independent_commissions",
        "probe": "Should independent commissions draw all electoral district boundaries?",
        "stance_A": "Yes, independent redistricting commissions are essential for fair elections. I've lived in districts that were obviously gerrymandered by partisan legislatures to benefit one party. Independent commissions create competitive districts that force candidates to appeal to all voters. The current system lets politicians choose their voters instead of voters choosing their politicians.",
        "stance_B": "No, so-called independent commissions aren't really independent and remove accountability from redistricting. I've seen 'nonpartisan' commissions dominated by former political operatives with clear biases. Elected legislators should control redistricting because they're accountable to voters. Geographic and community considerations matter more than abstract mathematical formulas.",
        "experiences_A": [
            "My congressional district was drawn to include three separate urban areas connected by highways, clearly designed to pack Democratic voters together.",
            "I worked on campaigns in our gerrymandered state legislature districts where the outcomes were predetermined and voter turnout was terrible.",
            "After our state adopted commission redistricting, we finally got competitive races and candidates who had to appeal to moderate voters."
        ],
        "experiences_B": [
            "Our 'independent' redistricting commission included three former Democratic staffers and two former Republican consultants, hardly nonpartisan.",
            "I watched the commission split our rural county between three districts using computer algorithms that ignored our agricultural community's shared interests.",
            "The commission process took months of closed-door meetings while legislative redistricting was done in public with hearings and votes."
        ],
        "reasoning_A": [
            "Bizarre district shapes prove partisan legislatures manipulate boundaries for electoral advantage rather than fair representation.",
            "Predetermined outcomes and low turnout show gerrymandering reduces democratic competition and voter engagement.",
            "Increased competitiveness after commission redistricting demonstrates the system produces fairer, more responsive representation."
        ],
        "reasoning_B": [
            "Commission composition bias shows 'independence' is often illusory and may simply hide political influence.",
            "Community splitting demonstrates how technical redistricting can ignore legitimate shared interests and local knowledge.",
            "Process opacity proves commissions can be less accountable than elected officials who face voter consequences."
        ],
        "category": "politics"
    },
    {
        "id": "voting_holiday_mandatory",
        "probe": "Should Election Day be a mandatory federal holiday with required paid time off?",
        "stance_A": "Yes, Election Day must be a mandatory federal holiday. I've seen too many working-class people unable to vote because they couldn't get time off work. Democracy requires equal access to voting, and our current system discriminates against hourly workers and people with inflexible jobs. Mandatory paid time off would dramatically increase turnout and representation.",
        "stance_B": "No, a mandatory voting holiday would be expensive and ineffective. I manage a small business and mandatory paid holidays create significant costs that hurt workers through reduced hours or layoffs. Early voting and mail-in ballots already solve access problems more efficiently. Many essential workers would still have to work anyway, so the holiday wouldn't help everyone.",
        "experiences_A": [
            "I worked retail during the 2020 election and had to choose between voting and missing a day's pay. My manager refused to give me time off.",
            "I volunteered at polls in working-class neighborhoods where turnout was much lower than in professional areas with flexible schedules.",
            "My night-shift coworker couldn't vote because polls closed before she woke up and opened after her shift started."
        ],
        "experiences_B": [
            "I run a restaurant and mandatory holidays already cost us thousands in overtime pay. Another one would force us to cut staff hours or raise prices.",
            "I voted early by mail three weeks before Election Day, which was more convenient than any holiday would be.",
            "I work in healthcare and we'd still have to staff the hospital on a voting holiday, so it wouldn't help medical workers anyway."
        ],
        "reasoning_A": [
            "Choosing between voting and pay demonstrates how current systems create economic barriers to democratic participation.",
            "Turnout disparities between different neighborhoods prove work schedule flexibility affects voting access unequally.",
            "Shift work conflicts show rigid Election Day timing prevents participation despite workers' desire to vote."
        ],
        "reasoning_B": [
            "Small business costs show mandatory holidays can harm the workers they're meant to help through reduced employment opportunities.",
            "Early voting convenience proves alternative solutions already address access problems more flexibly than holidays.",
            "Essential worker requirements demonstrate holidays don't solve access problems for many workers who must still work."
        ],
        "category": "politics"
    },
    {
        "id": "political_advertising_social_media_ban",
        "probe": "Should political advertising be banned on social media platforms?",
        "stance_A": "Yes, political ads should be banned from social media platforms. I've seen how microtargeted political ads spread misinformation and create filter bubbles that polarize society. Social media algorithms amplify divisive content for engagement, making them terrible venues for democratic discourse. Traditional media has editorial oversight and equal time rules that social platforms lack.",
        "stance_B": "No, banning political ads on social media would harm democratic participation. I've used Facebook ads to promote local candidates and ballot measures that traditional media ignored. Social media advertising is often the only way grassroots campaigns can reach voters affordably. Censoring political speech on major communication platforms threatens First Amendment rights.",
        "experiences_B": [
            "I managed a school board campaign with a $500 budget and Facebook ads were our only way to reach voters since local TV was too expensive.",
            "Our ballot measure for park funding got no newspaper coverage, but targeted social media ads helped us reach parents and dog owners who cared about the issue.",
            "I saw how quickly political ad bans could be expanded to limit legitimate advocacy by nonprofits and community groups."
        ],
        "experiences_A": [
            "I received targeted political ads claiming local ballot measures would raise my taxes by thousands of dollars, which fact-checkers proved false.",
            "I noticed my conservative relatives only saw ads supporting Republican candidates while I only saw Democratic ads, creating completely different information environments.",
            "I watched foreign actors buy Facebook ads to influence our local elections using fake American identities."
        ],
        "reasoning_A": [
            "False tax claims show how microtargeted ads can spread misinformation without traditional media fact-checking oversight.",
            "Different information environments demonstrate how algorithmic targeting creates polarizing filter bubbles that damage democratic discourse.",
            "Foreign interference proves social platforms lack sufficient verification systems to protect electoral integrity."
        ],
        "reasoning_B": [
            "Low-budget campaign success shows social media ads democratize political communication by reducing barriers for grassroots candidates.",
            "Ballot measure outreach proves social platforms can amplify important local issues that traditional media neglects.",
            "Censorship expansion concerns show restrictions on political advertising could threaten broader advocacy and free speech rights."
        ],
        "category": "politics"
    },
    {
        "id": "supreme_court_expansion",
        "probe": "Should Congress expand the Supreme Court beyond nine justices?",
        "stance_A": "Yes, the Supreme Court should be expanded to restore balance and legitimacy. I've watched the Court become increasingly partisan after Senate Republicans blocked Obama's nominee then rushed through Trump's picks. Nine justices is arbitrary - we've had different numbers before. Expansion would reduce the outsized impact of any single appointment and make the Court more representative of American values.",
        "stance_B": "No, expanding the Supreme Court would destroy its independence and legitimacy. I've seen how court-packing threats have been used throughout history to intimidate justices into political compliance. Once we start expanding for partisan advantage, each party will add more justices when they control government. The Court's stability and public trust depend on maintaining institutional norms.",
        "experiences_A": [
            "I watched Republican senators refuse to hold hearings for Merrick Garland for almost a year, then confirm Amy Coney Barrett in three weeks before an election.",
            "I've seen the Court overturn decades of precedent on issues like abortion and voting rights based on 5-4 partisan splits.",
            "I studied how we've had 6, 7, 8, and 10 justices in the past when Congress adjusted the Court size for practical reasons."
        ],
        "experiences_B": [
            "I remember FDR's court-packing scheme in the 1930s, which was widely seen as attacking judicial independence even by his own party members.",
            "I've watched how threats of court expansion have already changed judicial behavior, with some justices clearly worried about political retaliation.",
            "I studied countries where courts were expanded for political reasons and judicial independence collapsed within a generation."
        ],
        "reasoning_A": [
            "Confirmation timing disparities prove Republicans already broke institutional norms to capture the Court through partisan manipulation.",
            "Partisan voting patterns show the current Court operates more like a political body than an independent judiciary.",
            "Historical precedent demonstrates Court size changes are constitutional and have been used appropriately in the past."
        ],
        "reasoning_B": [
            "FDR's failed attempt shows even popular presidents face backlash when seen as attacking judicial independence.",
            "Changed judicial behavior proves expansion threats already undermine the Court's independence and decision-making integrity.",
            "International examples demonstrate how court manipulation leads to long-term institutional collapse and authoritarian control."
        ],
        "category": "politics"
    },
    {
        "id": "congressional_insider_trading_ban",
        "probe": "Should members of Congress be prohibited from trading individual stocks?",
        "stance_A": "Yes, Congress members should be completely banned from stock trading. I've tracked how representatives consistently outperform the market using information from committee hearings and private briefings. They vote on regulations that directly affect stock prices while holding those same stocks. This creates obvious conflicts of interest that undermine public trust in government.",
        "stance_B": "No, stock trading bans go too far and would discourage qualified people from serving. I know representatives who put their assets in blind trusts and follow disclosure rules carefully. The real solution is better enforcement of existing ethics rules and faster disclosure requirements. Blanket bans punish ethical behavior and don't address the real problem of inadequate oversight.",
        "experiences_A": [
            "I analyzed trading records and found several senators bought biotech stocks days before voting on FDA funding bills that boosted those companies.",
            "I watched a House member sell bank stocks the week before announcing new financial regulations that crashed those stock prices.",
            "I saw representatives get private COVID briefings in early 2020, then immediately trade on that information before the public knew the severity."
        ],
        "experiences_B": [
            "I worked for a congressman who put all investments in a blind trust managed by outside professionals with no input from him or his staff.",
            "I've seen how current disclosure rules work well when properly enforced - the problem is delayed reporting, not the trading itself.",
            "I know several potential candidates who chose private sector careers because government ethics rules would have destroyed their retirement savings through forced asset sales."
        ],
        "reasoning_A": [
            "Timing of biotech purchases before favorable votes shows members use non-public information for personal financial gain.",
            "Pre-announcement selling proves representatives profit from advance knowledge of their own regulatory actions.",
            "COVID trading demonstrates how privileged access to government information creates unfair market advantages."
        ],
        "reasoning_B": [
            "Blind trust usage shows ethical members can avoid conflicts while maintaining investment rights through proper safeguards.",
            "Disclosure effectiveness proves transparency can address concerns without blanket prohibitions on legal activity.",
            "Deterred candidates show overly restrictive rules could reduce the quality and diversity of people willing to serve in Congress."
        ],
        "category": "politics"
    },
    {
        "id": "electoral_college",
        "probe": "Should the United States abolish the Electoral College?",
        "stance_A": "Yes, the Electoral College is fundamentally undemocratic. I've seen how it makes voters in non-swing states feel their votes don't matter, depressing turnout and civic engagement. The system gives disproportionate power to smaller states and allows candidates to win without the popular vote. Every vote should count equally in a true democracy.",
        "stance_B": "No, the Electoral College protects federalism and ensures all states matter. I've witnessed how it forces candidates to build geographically diverse coalitions rather than just appealing to major cities. Without it, presidential campaigns would ignore entire regions of the country. The system preserves the balance between state and federal power that our founders intended.",
        "experiences_A": [
            "I lived in California and watched friends stop voting because they felt their votes were meaningless in a 'safe' state.",
            "Our local candidate won the popular vote by 3 million but still lost the election, which felt deeply unfair.",
            "I campaigned in Ohio and saw how swing state voters got disproportionate attention while other states were ignored."
        ],
        "experiences_B": [
            "I worked on a campaign that had to appeal to rural voters in Iowa and urban voters in Pennsylvania to win.",
            "My small state got meaningful attention from presidential candidates who otherwise would have skipped us entirely.",
            "I saw how candidates had to moderate their positions to appeal to diverse geographic constituencies."
        ],
        "reasoning_A": [
            "When citizens feel their votes don't count, it undermines democratic participation and legitimacy.",
            "Winning without the popular vote violates the basic democratic principle of majority rule.",
            "Unequal campaign attention shows the system makes some votes more valuable than others."
        ],
        "reasoning_B": [
            "Building diverse coalitions ensures presidents represent the whole country, not just population centers.",
            "Smaller states receiving attention demonstrates the system protects minority interests from majority tyranny.",
            "Moderating positions to appeal broadly creates more centrist, unifying leadership."
        ],
        "category": "politics"
    },
    {
        "id": "voter_id_requirements",
        "probe": "Should states require photo ID to vote?",
        "stance_A": "Yes, voter ID requirements are common sense security measures. I've worked elections and seen how easy it would be to impersonate someone without ID checks. Every other important transaction requires identification - banking, flying, even buying alcohol. Voter ID protects election integrity and builds public confidence in our democratic process.",
        "stance_B": "No, voter ID laws are voter suppression in disguise. I've helped elderly and low-income citizens who struggled to get the required documents and couldn't vote as a result. These laws disproportionately affect marginalized communities who are less likely to have driver's licenses. The actual fraud these laws prevent is virtually nonexistent.",
        "experiences_A": [
            "I was a poll worker and someone could have easily voted using my neighbor's name with no verification.",
            "Our state implemented voter ID and public trust in elections increased significantly according to polling.",
            "I needed photo ID to pick up my mail-in ballot, which seemed like a reasonable security measure."
        ],
        "experiences_B": [
            "I helped an 80-year-old woman who couldn't vote because she didn't have a driver's license and couldn't get to the DMV.",
            "Our community saw a 15% drop in turnout among Black and Hispanic voters after ID laws passed.",
            "I researched voter fraud cases and found only 31 credible instances out of over 1 billion votes cast."
        ],
        "reasoning_A": [
            "The ease of impersonation without ID verification shows a genuine security vulnerability in the voting process.",
            "Increased public confidence demonstrates these measures strengthen democratic legitimacy.",
            "Using ID for ballot collection shows even mail voting benefits from identity verification."
        ],
        "reasoning_B": [
            "Elderly citizens unable to obtain ID demonstrates these laws create barriers for eligible voters.",
            "Disproportionate impact on minority communities shows these laws have discriminatory effects.",
            "The tiny fraud rate proves the problem these laws claim to solve barely exists."
        ],
        "category": "politics"
    },
    {
        "id": "campaign_finance_limits",
        "probe": "Should there be strict limits on campaign donations and spending?",
        "stance_A": "Yes, unlimited campaign spending corrupts democracy. I've seen how wealthy donors get special access while ordinary citizens are shut out of the political process. Big money drowns out regular voters' voices and creates a system where politicians serve their funders rather than constituents. Democracy should be about ideas, not bank accounts.",
        "stance_B": "No, campaign spending is protected political speech. I've donated to causes I believe in and consider it my fundamental right to support candidates. Spending limits favor incumbents and established media while restricting grassroots movements. The solution to speech you disagree with is more speech, not censorship through spending caps.",
        "experiences_A": [
            "I attended a fundraiser where donors paid $10,000 for face time with senators while constituents got form letters.",
            "Our local candidate was outspent 20-to-1 by corporate money and lost despite better ideas and community support.",
            "I watched pharmaceutical companies spend millions to defeat a drug pricing bill that had 80% public support."
        ],
        "experiences_B": [
            "I donated $500 to help an outsider candidate compete against the party establishment's preferred choice.",
            "Our grassroots movement raised money online to run ads the mainstream media wouldn't cover.",
            "I saw how spending limits in our city elections helped incumbents who already had name recognition."
        ],
        "reasoning_A": [
            "Exclusive donor access demonstrates how money creates unequal political influence and representation.",
            "Being massively outspent shows how unlimited money can overcome popular support and better policies.",
            "Corporate spending defeating popular legislation proves money subverts democratic will."
        ],
        "reasoning_B": [
            "Supporting outsider candidates shows donations enable political competition and voter choice.",
            "Funding alternative messaging demonstrates spending enables speech that wouldn't otherwise be heard.",
            "Incumbent advantages under spending limits prove restrictions can reduce rather than increase competition."
        ],
        "category": "politics"
    },
    {
        "id": "gerrymandering_reform",
        "probe": "Should redistricting be handled by independent commissions rather than state legislatures?",
        "stance_A": "Yes, independent commissions would end partisan gerrymandering. I've seen how legislators draw districts that look like abstract art to protect their own seats and eliminate competition. When politicians choose their voters instead of voters choosing politicians, democracy breaks down. Independent redistricting would create fair maps and competitive elections.",
        "stance_B": "No, elected legislators should control redistricting because they're accountable to voters. I've seen how supposedly 'independent' commissions still make political choices about communities of interest and district priorities. At least with legislative redistricting, voters can hold mapmakers accountable. There's no such thing as truly neutral redistricting - it's inherently political.",
        "experiences_A": [
            "I live in a district that snakes 200 miles to connect Republican suburbs while splitting our city in half.",
            "Our state's maps created 12 safe seats for each party with only 1 competitive district out of 25 total.",
            "I campaigned in bizarrely shaped districts where candidates ignored 80% of voters in 'safe' areas."
        ],
        "experiences_B": [
            "I served on our 'nonpartisan' redistricting commission and watched members make clearly political decisions about district lines.",
            "Our state legislature changed the maps after public hearings showed problems with the initial commission proposal.",
            "I saw how commission members were selected by the same politicians people wanted to remove from the process."
        ],
        "reasoning_A": [
            "Bizarre district shapes demonstrate how partisan control creates maps designed for political advantage rather than fair representation.",
            "Safe seats with no competition show how gerrymandering eliminates meaningful voter choice.",
            "Candidates ignoring most voters proves gerrymandering reduces democratic accountability."
        ],
        "reasoning_B": [
            "Political decisions by 'nonpartisan' commissioners show that redistricting inevitably involves subjective political choices.",
            "Legislative responsiveness to public input demonstrates elected officials provide better accountability than appointed commissioners.",
            "Political selection of commissioners reveals that 'independent' bodies aren't actually removed from political influence."
        ],
        "category": "politics"
    },
    {
        "id": "marijuana_legalization",
        "probe": "Should marijuana be legalized for recreational use nationwide?",
        "stance_A": "Yes, marijuana prohibition has failed and causes more harm than the drug itself. I've seen how criminalization destroys lives through incarceration while creating dangerous black markets. Legal regulation would ensure product safety, generate tax revenue, and allow law enforcement to focus on serious crimes. Adults should have the freedom to make their own choices.",
        "stance_B": "No, marijuana legalization increases usage and creates public health problems. I've witnessed more impaired driving and youth access in states that legalized. The drug affects brain development and can trigger mental health issues, especially in teenagers. Just because something is popular doesn't mean it should be legal - we need to protect public safety and health.",
        "experiences_A": [
            "I knew someone who went to prison for marijuana possession and lost their job, housing, and family relationships.",
            "Our city's dispensary system generates significant tax revenue while eliminating dangerous street dealers.",
            "I saw how marijuana arrests disproportionately affected Black and Hispanic communities despite similar usage rates across races."
        ],
        "experiences_B": [
            "I'm a police officer who's seen a 40% increase in marijuana-impaired driving accidents since legalization.",
            "My teenage nephew easily obtained high-potency marijuana products from legal dispensaries using fake IDs.",
            "I work in mental health and treat more young people with marijuana-induced psychosis in legal states."
        ],
        "reasoning_A": [
            "Imprisonment for possession destroying lives shows prohibition creates punishments worse than the crime.",
            "Tax revenue and eliminating dealers demonstrates legalization provides better outcomes than prohibition.",
            "Racial disparities in enforcement prove prohibition enables discriminatory law enforcement."
        ],
        "reasoning_B": [
            "Increased impaired driving accidents shows legalization creates genuine public safety risks.",
            "Easy youth access despite regulations proves legal markets struggle to prevent underage use.",
            "Rising marijuana-induced mental health issues demonstrates legalization increases harmful health outcomes."
        ],
        "category": "politics"
    },
    {
        "id": "minimum_wage_increase",
        "probe": "Should the federal minimum wage be raised to $15 per hour?",
        "stance_A": "Yes, the current minimum wage is poverty wages that force workers to choose between rent and food. I've seen full-time employees needing food stamps and working multiple jobs just to survive. A $15 minimum wage would lift millions out of poverty and stimulate the economy as workers spend their increased earnings. No one working full-time should live in poverty.",
        "stance_B": "No, a $15 minimum wage would kill jobs and hurt the workers it's meant to help. I've run small businesses and seen how labor cost increases force difficult choices between laying off workers and raising prices. Entry-level positions would disappear, making it harder for inexperienced workers to get started. Market forces, not government mandates, should determine wages.",
        "experiences_A": [
            "I worked full-time at minimum wage and still needed food assistance to feed my children.",
            "Our city raised the minimum wage and local workers saw immediate improvements in housing stability and healthcare access.",
            "I managed a retail store where turnover dropped 60% after we voluntarily raised wages to $15."
        ],
        "experiences_B": [
            "I owned a restaurant and had to lay off three workers when the city mandated a $15 minimum wage.",
            "Our family business raised prices 20% to cover higher labor costs and lost customers to chain competitors.",
            "I saw teenagers lose summer job opportunities because employers couldn't justify $15 for inexperienced workers."
        ],
        "reasoning_A": [
            "Needing food assistance while working full-time demonstrates current wages are insufficient for basic survival.",
            "Improved housing stability and healthcare access shows higher wages directly improve worker wellbeing.",
            "Reduced turnover proves higher wages can improve business operations and worker retention."
        ],
        "reasoning_B": [
            "Laying off workers shows higher minimum wages can reduce total employment opportunities.",
            "Price increases and lost customers demonstrate how wage mandates can hurt business competitiveness.",
            "Lost youth employment opportunities prove higher minimums can eliminate entry-level positions."
        ],
        "category": "politics"
    },
    {
        "id": "healthcare_single_payer",
        "probe": "Should the United States adopt a single-payer healthcare system?",
        "stance_A": "Yes, single-payer would provide universal coverage while controlling costs. I've seen people ration insulin and skip cancer treatments because of insurance costs and deductibles. Our current system wastes billions on insurance company profits and administrative overhead. Every other developed country proves that government-run healthcare delivers better outcomes at lower costs.",
        "stance_B": "No, single-payer would reduce quality and eliminate choice while increasing government control. I've experienced excellent care through private insurance and don't want government bureaucrats making my medical decisions. Wait times would increase and innovation would decrease without market competition. The government can't even run the VA properly - why trust them with everyone's healthcare?",
        "experiences_A": [
            "I watched my diabetic neighbor ration insulin because his insurance deductible reset and he couldn't afford $300 monthly copays.",
            "Our family went bankrupt from cancer treatment costs despite having 'good' insurance with high deductibles.",
            "I spent hours fighting with insurance companies to get approval for my doctor's recommended treatment."
        ],
        "experiences_B": [
            "I received world-class cancer treatment through my employer's insurance plan with minimal wait times.",
            "My veteran friend waited eight months for knee surgery through the VA while I got mine in two weeks privately.",
            "I chose a high-deductible plan that saved money and gave me control over my healthcare spending."
        ],
        "reasoning_A": [
            "Insulin rationing due to costs shows private insurance fails to ensure access to essential medications.",
            "Medical bankruptcy despite insurance proves the current system provides inadequate financial protection.",
            "Fighting for treatment approval demonstrates how private insurers obstruct medical care."
        ],
        "reasoning_B": [
            "Excellent private care with short waits shows market-based systems can deliver high-quality, timely treatment.",
            "Long VA wait times compared to private care suggest government-run systems reduce efficiency and access.",
            "Successful use of high-deductible plans demonstrates private insurance offers valuable choice and cost control."
        ],
        "category": "politics"
    },
    {
        "id": "police_reform_funding",
        "probe": "Should cities redirect police funding to social services and mental health programs?",
        "stance_A": "Yes, we're asking police to solve problems they're not trained for while underfunding the services that actually address root causes. I've seen officers respond to mental health crises they're not equipped to handle, often making situations worse. Investing in education, housing, and healthcare would prevent crime more effectively than increasing arrests and incarceration.",
        "stance_B": "No, reducing police funding would increase crime and hurt the communities that need protection most. I've lived in high-crime neighborhoods where more police presence made the difference between safety and chaos. Social services are important but can't replace law enforcement when crimes are actually being committed. Public safety requires adequate police resources and training.",
        "experiences_A": [
            "I watched police escalate a mental health crisis that social workers later resolved peacefully in 20 minutes.",
            "Our neighborhood's crime rate dropped after the city invested in youth programs and job training rather than more patrols.",
            "I saw officers spending most of their time on homelessness and addiction issues they weren't trained to address."
        ],
        "experiences_B": [
            "I lived in an area where reduced police presence led to a 30% increase in break-ins and robberies.",
            "My elderly mother feels safer walking at night because of increased police patrols in her neighborhood.",
            "I called 911 during a domestic violence incident and needed immediate police response, not a social worker."
        ],
        "reasoning_A": [
            "Police escalation of mental health situations shows officers lack appropriate training for non-criminal emergencies.",
            "Crime reduction through social investment proves prevention is more effective than enforcement.",
            "Officers handling issues outside their expertise demonstrates misallocation of public safety resources."
        ],
        "reasoning_B": [
            "Increased crime following reduced police presence shows law enforcement deters criminal activity.",
            "Elderly residents feeling safer with patrols demonstrates police provide valuable community security.",
            "Needing immediate police response for violence shows some situations require law enforcement intervention."
        ],
        "category": "politics"
    },
    {
        "id": "climate_carbon_tax",
        "probe": "Should the government implement a carbon tax to address climate change?",
        "stance_A": "Yes, a carbon tax would harness market forces to drive clean energy innovation and reduce emissions. I've seen how putting a price on pollution creates immediate incentives for businesses to find cleaner alternatives. The revenue could fund renewable energy development and provide rebates to offset costs for working families. We need market-based solutions to this urgent crisis.",
        "stance_B": "No, a carbon tax would hurt working families and destroy American jobs while accomplishing nothing globally. I've watched manufacturing jobs move overseas to countries with lower environmental standards when regulations increase costs here. Higher energy costs hit the poor hardest while wealthy people can afford to pay more. China and India won't follow our lead, making this economic self-harm.",
        "experiences_A": [
            "I work for a company that invested heavily in energy efficiency after our state implemented carbon pricing.",
            "Our provincial carbon tax generated billions in revenue that funded transit improvements and home energy rebates.",
            "I've seen how carbon pricing in Europe drove rapid development of renewable energy technologies."
        ],
        "experiences_B": [
            "I lost my job at a steel plant that moved operations to Mexico partly due to environmental compliance costs.",
            "Our family's heating bills increased 25% after the state added carbon fees to natural gas.",
            "I watched China increase coal production while we debated carbon taxes that would handicap American industry."
        ],
        "reasoning_A": [
            "Company investment in efficiency shows carbon pricing creates market incentives for emission reductions.",
            "Revenue funding transit and rebates demonstrates carbon taxes can be designed to benefit citizens.",
            "European renewable development proves carbon pricing accelerates clean energy innovation."
        ],
        "reasoning_B": [
            "Job losses to lower-regulation countries show carbon taxes can drive away American manufacturing.",
            "Increased heating costs demonstrate carbon taxes impose regressive burdens on working families.",
            "China's continued coal use proves unilateral carbon pricing provides no global climate benefit."
        ],
        "category": "politics"
    },
    {
        "id": "parental_social_media_monitoring",
        "probe": "Should parents monitor their children's social media activity?",
        "stance_A": "Yes, parents must monitor their children's social media for their safety. I caught my 13-year-old daughter being contacted by an adult predator through her Instagram DMs, and monitoring saved her from potential harm. Children don't understand the dangers online - from cyberbullying to predators to permanent reputation damage. Active monitoring is basic parental responsibility in the digital age.",
        "stance_B": "No, monitoring social media violates children's privacy and damages trust. When my parents read through all my messages as a teenager, it destroyed our relationship for years and made me more secretive, not safer. Kids need space to develop independence and learn from mistakes. Constant surveillance teaches them to hide things rather than communicate openly about problems.",
        "experiences_A": [
            "I caught my 13-year-old being contacted by an adult predator through Instagram monitoring. I reported it to police.",
            "My monitoring revealed my son was being severely cyberbullied at school. We addressed it before he became suicidal.",
            "I found my daughter sharing personal information that could have led to identity theft or stalking."
        ],
        "experiences_B": [
            "My parents monitored all my social media as a teen. It destroyed our trust and made me hide everything from them.",
            "I became an expert at using secret apps and deleting messages. The monitoring made me more deceptive, not safer.",
            "My friend's parents' constant surveillance drove him to dangerous real-world rebellion they never detected."
        ],
        "reasoning_A": [
            "The predator contact shows children face real dangers online that only parental oversight can catch.",
            "The cyberbullying intervention demonstrates monitoring can identify serious mental health risks early.",
            "The information sharing reveals children lack judgment about privacy that could have serious consequences."
        ],
        "reasoning_B": [
            "The broken trust shows monitoring damages the parent-child relationship needed for real safety.",
            "The increased deception proves surveillance makes children more secretive rather than protecting them.",
            "The undetected rebellion demonstrates that determined children will find dangerous outlets monitoring can't catch."
        ],
        "category": "ethics"
    },
    {
        "id": "end_of_life_medical_decisions",
        "probe": "Should terminally ill patients have the right to physician-assisted death?",
        "stance_A": "Yes, terminally ill patients deserve the right to die with dignity on their own terms. I watched my father suffer through months of agony from pancreatic cancer, begging to die but legally unable to get help. No one should be forced to endure unbearable pain when there's no hope of recovery. Compassionate medical assistance for those who choose it is the humane approach.",
        "stance_B": "No, physician-assisted death crosses a dangerous line that threatens vulnerable patients. I've seen elderly patients pressure themselves to 'not be a burden' when they could have had meaningful time left. My grandmother talked about wanting to die during chemo, but she recovered and had five more good years with us. Medical professionals should heal and comfort, never participate in ending life.",
        "experiences_A": [
            "My father suffered months of unbearable pain from pancreatic cancer, begging to die but legally unable to get help ending his suffering.",
            "I watched my aunt waste away from ALS, losing all dignity and autonomy while her mind remained sharp and trapped.",
            "My neighbor had to travel to another country for assisted death because our laws forced unnecessary suffering."
        ],
        "experiences_B": [
            "My grandmother wanted to die during chemo but recovered and had five wonderful years with our family afterward.",
            "I saw elderly patients at the hospital pressure themselves to 'not be a burden' when they had treatable conditions.",
            "My friend's mother was pushed toward assisted death by family members who wanted her inheritance money."
        ],
        "reasoning_A": [
            "The prolonged suffering shows that forcing patients to endure pain violates their autonomy and dignity.",
            "The loss of function with retained consciousness demonstrates some conditions create unbearable quality of life.",
            "The need to travel shows current laws force additional trauma on families facing terminal illness."
        ],
        "reasoning_B": [
            "The recovery after despair proves patients' wishes during crisis may not reflect their true long-term interests.",
            "The self-imposed pressure shows vulnerable patients may choose death due to social factors rather than medical necessity.",
            "The family coercion reveals how financial motives could corrupt medical decisions about ending life."
        ],
        "category": "ethics"
    },
    {
        "id": "mandatory_vaccination_public_health",
        "probe": "Should vaccination be mandatory for children attending public schools?",
        "stance_A": "Yes, mandatory vaccination is essential for protecting public health. I saw how measles outbreaks devastated our school district when vaccination rates dropped, putting immunocompromised children at deadly risk. Vaccines are among the safest and most effective medical interventions we have. Personal choice ends when it threatens the health and lives of other people's children.",
        "stance_B": "No, mandatory vaccination violates parental rights and bodily autonomy. My son had a severe allergic reaction to his first vaccine that hospitalized him, and I should have the right to make informed medical decisions for my family. Many vaccines contain ingredients some families avoid for religious or health reasons. Medical decisions should remain between parents and their doctors.",
        "experiences_A": [
            "Our school had a measles outbreak that hospitalized three children when vaccination rates dropped below herd immunity levels.",
            "I watched my immunocompromised daughter have to stay home for weeks during a pertussis outbreak at her school.",
            "My pediatrician showed me statistics proving vaccines eliminated diseases that used to kill thousands of children annually."
        ],
        "experiences_B": [
            "My son had a severe allergic reaction to his first vaccine that required emergency hospitalization and ongoing treatment.",
            "Our religious beliefs prohibit certain medical interventions, and the state shouldn't override our faith-based parenting decisions.",
            "I researched vaccine ingredients and found chemicals I don't want injected into my healthy child's body."
        ],
        "reasoning_A": [
            "The outbreak demonstrates how individual vaccine refusal can create community-wide health crises.",
            "The immunocompromised child's isolation shows vaccination protects the most vulnerable through herd immunity.",
            "The historical disease elimination proves vaccines' effectiveness at preventing childhood deaths."
        ],
        "reasoning_B": [
            "The severe reaction shows vaccines do carry real risks that parents should be able to assess individually.",
            "The religious conflict demonstrates mandatory vaccination can violate fundamental constitutional freedoms.",
            "The ingredient concerns show parents may have legitimate medical reasons for avoiding certain vaccines."
        ],
        "category": "ethics"
    },
    {
        "id": "corporate_political_donations",
        "probe": "Should corporations be prohibited from making political donations?",
        "stance_A": "Yes, corporate political donations corrupt democracy and give wealthy interests disproportionate power. I worked for a company that donated millions to candidates who then voted for tax breaks that saved us even more millions. This isn't free speech - it's legalized bribery that drowns out ordinary citizens' voices. Democracy should be about people, not corporate profit maximization.",
        "stance_B": "No, prohibiting corporate political donations violates free speech and ignores economic realities. I run a small business and corporate donations help elect candidates who understand job creation and economic growth. Corporations employ millions of people and drive economic activity - they should have a voice in policies that affect them. Restricting speech based on the speaker's identity is fundamentally undemocratic.",
        "experiences_A": [
            "My company donated millions to candidates who then voted for tax breaks that saved us even more. It was clearly pay-to-play.",
            "I watched pharmaceutical companies buy influence to block drug pricing reforms that would have helped patients but hurt profits.",
            "Our union's small donations were overwhelmed by corporate money backing anti-worker candidates who won purely through spending."
        ],
        "experiences_B": [
            "Corporate donations helped elect pro-business candidates who reduced regulations that were killing small businesses like mine.",
            "I saw environmental groups get outspent by energy companies, but that's how free speech works - everyone gets to participate.",
            "Our industry's political donations prevented job-killing legislation that would have moved manufacturing overseas."
        ],
        "reasoning_A": [
            "The quid pro quo relationship shows corporate donations create direct corruption of democratic processes.",
            "The blocked reforms demonstrate how corporate money prevents policies that would benefit the public interest.",
            "The spending disparity proves corporate donations give wealthy interests unequal political influence."
        ],
        "reasoning_B": [
            "The regulatory relief shows corporate political participation can produce beneficial economic outcomes.",
            "The competitive spending acknowledges that free speech means all groups can advocate for their interests.",
            "The prevented job losses demonstrate corporate donations can protect legitimate economic interests."
        ],
        "category": "ethics"
    },
    {
        "id": "genetic_privacy_insurance",
        "probe": "Should insurance companies be allowed to use genetic test results in coverage decisions?",
        "stance_A": "Yes, insurance companies should be able to use genetic information just like any other health data. I work in insurance and genetic testing helps us price risk accurately and prevent fraud. If someone knows they have a genetic predisposition to expensive diseases but hides it, they're essentially forcing other policyholders to subsidize their costs. Fair pricing requires full information about health risks.",
        "stance_B": "No, genetic discrimination by insurers would create a permanent underclass of uninsurable people. I have the BRCA gene mutation that increases breast cancer risk, but I haven't developed cancer and may never will. Denying coverage based on genetic possibilities rather than actual illness punishes people for their biology and discourages life-saving genetic testing.",
        "experiences_A": [
            "I work in insurance underwriting and genetic testing helps us identify high-risk applicants who would otherwise hide expensive conditions.",
            "Our company found several cases where people got genetic tests showing Huntington's disease, then immediately bought large life insurance policies.",
            "Genetic information prevents adverse selection where only sick people buy insurance, which would bankrupt the system."
        ],
        "experiences_B": [
            "I have the BRCA mutation but haven't developed cancer. Insurance companies wanted to charge me triple or deny coverage entirely.",
            "My friend delayed genetic testing for Huntington's disease because she was afraid of losing her health insurance.",
            "Genetic discrimination would create a permanent class of uninsurable people punished for their DNA."
        ],
        "reasoning_A": [
            "The hidden conditions show genetic information prevents fraud and ensures accurate risk assessment.",
            "The immediate policy purchases demonstrate how genetic knowledge creates adverse selection against insurers.",
            "The systemic risk shows genetic restrictions could destabilize insurance markets for everyone."
        ],
        "reasoning_B": [
            "The coverage denial shows genetic information can make insurance unaffordable for people who aren't actually sick.",
            "The delayed testing proves genetic discrimination discourages preventive medicine that could save lives.",
            "The systematic exclusion demonstrates genetic discrimination would create permanent healthcare inequality."
        ],
        "category": "ethics"
    },
    {
        "id": "cultural_appropriation_business",
        "probe": "Should businesses be restricted from using cultural elements from communities they don't belong to?",
        "stance_A": "Yes, businesses should face restrictions on cultural appropriation because it's economic exploitation of marginalized communities. I watched a major fashion company steal my grandmother's traditional textile designs and make millions while our Native community remained impoverished. Cultural appropriation extracts value from our heritage while giving nothing back to the people who created and preserved these traditions.",
        "stance_B": "No, restricting cultural use in business would stifle creativity and create impossible enforcement standards. I run a fusion restaurant that celebrates multiple cultures, and customers love how we blend traditions respectfully. Culture naturally evolves through mixing and sharing - trying to police who can use what cultural elements would fragment society and kill innovation. Appreciation shouldn't be confused with appropriation.",
        "experiences_A": [
            "A major fashion company copied my grandmother's traditional designs and made millions while our reservation stayed poor.",
            "I saw yoga studios profit from ancient practices while ignoring the spiritual context and Hindu origins.",
            "A brewery used sacred Native symbols on beer labels despite our community's requests to stop."
        ],
        "experiences_B": [
            "My fusion restaurant celebrates multiple cultures respectfully and customers from all backgrounds appreciate the cultural blending.",
            "I learned traditional techniques from immigrant craftspeople who were happy to share their knowledge and earn income.",
            "Trying to police cultural usage would mean banning most music, food, and art that makes modern culture vibrant."
        ],
        "reasoning_A": [
            "The copied designs show how businesses can profit from cultural heritage while the originating communities receive no benefit.",
            "The decontextualized yoga demonstrates how commercialization can strip away sacred meaning from cultural practices.",
            "The ignored requests prove businesses often continue appropriation despite objections from affected communities."
        ],
        "reasoning_B": [
            "The successful fusion restaurant shows cultural mixing can be done respectfully and appreciated by diverse communities.",
            "The collaborative learning demonstrates cultural exchange can benefit both teachers and students economically.",
            "The broad cultural impact shows restriction would eliminate beneficial cultural innovation and artistic expression."
        ],
        "category": "ethics"
    },
    {
        "id": "tech_worker_military_contracts",
        "probe": "Should tech workers have the right to refuse military contract work based on ethical objections?",
        "stance_A": "Yes, tech workers should absolutely have the right to refuse military contracts that violate their conscience. I quit my job at a defense contractor when I learned our AI software was being used for autonomous weapons targeting. Engineers shouldn't be forced to build technology that kills people if it conflicts with their moral beliefs. Professional autonomy includes the right to ethical objection.",
        "stance_B": "No, employees don't get to pick and choose which legal contracts their company fulfills based on personal politics. I work in tech and our military contracts help defend democracy and protect American lives overseas. If workers can veto any project they dislike, companies couldn't function and national security would suffer. Personal beliefs shouldn't override professional responsibilities.",
        "experiences_A": [
            "I quit my defense contractor job when I learned our AI was being used for autonomous weapons targeting civilians.",
            "Our team was asked to build surveillance software for authoritarian regimes. Several engineers refused and were reassigned.",
            "I watched colleagues develop drone technology that later killed innocent people in airstrikes."
        ],
        "experiences_B": [
            "I work on military contracts that help protect soldiers' lives through better communication and navigation systems.",
            "Our cybersecurity work for defense agencies protects critical infrastructure from foreign attacks.",
            "If engineers could veto projects, our company couldn't fulfill contracts that strengthen national security."
        ],
        "reasoning_A": [
            "The autonomous weapons application shows how tech work can directly enable lethal force that violates human rights.",
            "The successful reassignment demonstrates companies can accommodate ethical objections without major disruption.",
            "The civilian casualties prove military technology can cause harm that conflicts with engineers' moral values."
        ],
        "reasoning_B": [
            "The protective applications show military contracts often serve defensive rather than offensive purposes.",
            "The infrastructure protection demonstrates how military tech work can serve broader public safety interests.",
            "The contract fulfillment concern shows individual objections could undermine legitimate national security needs."
        ],
        "category": "ethics"
    },
    {
        "id": "algorithmic_hiring_bias",
        "probe": "Should companies be required to audit their hiring algorithms for discriminatory bias?",
        "stance_A": "Yes, algorithmic hiring audits are essential to prevent systematic discrimination. I discovered our company's AI screening tool was rejecting qualified Black candidates at twice the rate of white applicants with identical qualifications. These systems perpetuate historical bias unless we actively monitor and correct them. Required audits would force companies to confront and fix discriminatory algorithms they might otherwise ignore.",
        "stance_B": "No, mandatory algorithm audits would burden companies with expensive compliance theater while missing real discrimination. I've seen audit requirements that focus on statistical parity rather than actual fairness, forcing us to hire less qualified candidates to meet quotas. Human bias in hiring is often worse than algorithmic bias, and these audits would push companies away from potentially fairer automated systems.",
        "experiences_A": [
            "Our AI screening tool rejected qualified Black candidates at twice the rate of white applicants with identical qualifications.",
            "I found our algorithm penalized resumes with 'foreign-sounding' names even when experience was superior.",
            "Our hiring system trained on historical data replicated past discrimination against women in technical roles."
        ],
        "experiences_B": [
            "Audit requirements forced us to hire less qualified candidates to meet statistical parity rather than finding actual bias.",
            "I've seen human recruiters show worse bias than our algorithms, but only the AI gets scrutinized.",
            "Compliance costs for algorithm audits would push us back to subjective human hiring that's even more discriminatory."
        ],
        "reasoning_A": [
            "The racial disparities prove algorithms can systematically discriminate against qualified candidates without detection.",
            "The name-based bias shows how subtle algorithmic discrimination can perpetuate ethnic prejudice.",
            "The gender replication demonstrates how historical data can embed past discrimination in new systems."
        ],
        "reasoning_B": [
            "The quota pressure shows audits may prioritize statistical outcomes over genuine fairness or qualifications.",
            "The human comparison reveals audits create double standards that don't address broader hiring bias.",
            "The compliance burden suggests audit requirements could eliminate potentially fairer automated systems."
        ],
        "category": "ethics"
    },
    {
        "id": "mandatory_organ_donation",
        "probe": "Should organ donation be mandatory upon death unless explicitly opted out?",
        "stance_A": "Yes, organ donation should be opt-out rather than opt-in. I've seen too many patients die waiting for organs while perfectly healthy organs are buried or cremated. Most people support donation in principle but never complete the paperwork. An opt-out system respects individual choice while saving thousands of lives through better default policies.",
        "stance_B": "No, organ donation must remain opt-in only. I believe bodily autonomy is fundamental - the state cannot claim ownership of our bodies, even after death. Many families need time to process grief and make informed decisions about their loved one's remains. Mandatory systems, even with opt-outs, violate religious and cultural beliefs about bodily integrity.",
        "experiences_A": [
            "I watched a 16-year-old die waiting for a kidney while three compatible donors were buried that week without donating.",
            "Our hospital implemented an opt-out donor registry and organ availability increased 40% with no complaints from families.",
            "I counseled a mother whose son needed a heart transplant. She couldn't understand why healthy organs were being wasted."
        ],
        "experiences_B": [
            "A family came to me distraught that their father's organs were harvested before they could say goodbye properly.",
            "I worked with immigrant communities who feared opt-out systems would target their bodies for wealthy recipients.",
            "My own religious tradition requires intact burial. An opt-out system would burden us with constant bureaucratic vigilance."
        ],
        "reasoning_A": [
            "The teenage death illustrates how the current opt-in system fails due to administrative barriers rather than actual preferences.",
            "The 40% increase proves opt-out systems dramatically improve organ availability without coercing unwilling participants.",
            "The mother's question highlights the moral tragedy of wasting life-saving organs due to paperwork failures."
        ],
        "reasoning_B": [
            "The family's distress shows opt-out systems can override important cultural practices around death and grieving.",
            "The immigrant community's fear reveals how mandatory systems can create disparities and exploit vulnerable populations.",
            "The religious burial requirement demonstrates how opt-out policies burden minority beliefs with additional administrative steps."
        ],
        "category": "ethics"
    },
    {
        "id": "parental_genetic_enhancement",
        "probe": "Should parents be allowed to genetically enhance their children's traits?",
        "stance_A": "Yes, parents should have the right to genetically enhance their children. I've seen families devastated by preventable genetic diseases that we now have the technology to eliminate. Parents already make countless decisions about their children's future - from education to medical care. If we can give children better health, intelligence, or physical capabilities, denying that option seems cruel and arbitrary.",
        "stance_B": "No, genetic enhancement of children should not be allowed. I worry about creating a genetic class system where enhanced children have unfair advantages over natural ones. We don't understand the long-term consequences of genetic modifications, and children cannot consent to permanent alterations. This technology will increase inequality and pressure all parents to enhance or disadvantage their kids.",
        "experiences_A": [
            "I counseled a family with Huntington's disease who could eliminate it from their bloodline using genetic editing.",
            "My colleague's daughter was born with enhanced intelligence genes and is thriving academically beyond her peers.",
            "I researched genetic modifications that could prevent my future children from inheriting my family's diabetes and heart disease."
        ],
        "experiences_B": [
            "I saw a documentary about Chinese designer babies where the scientist was imprisoned and the children's futures became uncertain.",
            "My friend feels pressured to genetically enhance her pregnancy because other parents in her social circle are doing it.",
            "I read about genetic modifications that had unexpected side effects appearing only years later in animal studies."
        ],
        "reasoning_A": [
            "Eliminating Huntington's disease prevents certain suffering and death, making genetic intervention a clear moral good.",
            "The enhanced intelligence success shows genetic improvements can provide real benefits without apparent harm.",
            "Preventing inherited diseases demonstrates genetic enhancement as an extension of responsible parental healthcare decisions."
        ],
        "reasoning_B": [
            "The imprisoned scientist case shows genetic enhancement lacks proper safety protocols and regulatory oversight.",
            "The social pressure situation reveals how enhancement creates coercive environments forcing all parents to participate.",
            "The delayed side effects in animals prove we don't understand the long-term consequences of genetic modifications."
        ],
        "category": "ethics"
    },
    {
        "id": "elder_care_obligations",
        "probe": "Should adult children be legally required to care for their aging parents?",
        "stance_A": "Yes, adult children should have legal obligations to care for aging parents. I grew up in a culture where family responsibility is paramount, and I've seen how this creates stronger communities. My parents sacrificed everything for my education and opportunities. Legal frameworks ensure that elderly people aren't abandoned and that family bonds remain meaningful rather than optional.",
        "stance_B": "No, elder care should not be a legal requirement for adult children. I've witnessed too many toxic family situations where mandatory care would be harmful to everyone involved. Some parents were abusive or absent, and forcing care relationships creates resentment. Quality elder care requires willing participation - forced caregiving leads to neglect and emotional abuse.",
        "experiences_A": [
            "I care for my mother with dementia and can't imagine abandoning her after she raised me for 18 years.",
            "My neighbor's elderly father was placed in a quality facility by his children who visit daily and manage his care.",
            "I witnessed an elderly woman living alone whose children moved away and never called - legal obligations might have prevented this neglect."
        ],
        "experiences_B": [
            "I know someone forced to care for their alcoholic father who had been physically abusive throughout their childhood.",
            "My friend's mental health deteriorated severely while caring for a parent with Alzheimer's - she had no other siblings to share the burden.",
            "I saw a family where legal care requirements led to financial exploitation of the elderly parent by resentful adult children."
        ],
        "reasoning_A": [
            "The dementia care shows how family obligations can provide loving, personal care that reflects natural gratitude and reciprocity.",
            "The facility placement demonstrates that legal requirements don't mean personal care - they ensure responsible oversight and involvement.",
            "The abandoned elderly woman illustrates how legal frameworks could prevent elder neglect and maintain family accountability."
        ],
        "reasoning_B": [
            "The abusive father situation shows how legal requirements can trap victims in continued harmful relationships.",
            "The mental health deterioration proves that forced caregiving can damage both caregiver and patient when the burden is unsustainable.",
            "The financial exploitation case reveals how legal obligations can enable elder abuse rather than prevent it."
        ],
        "category": "ethics"
    },
    {
        "id": "truth_telling_terminal_illness",
        "probe": "Should doctors always tell patients they have a terminal illness?",
        "stance_A": "Yes, doctors should always tell patients about terminal diagnoses. I believe patients have an absolute right to know their medical condition and make informed decisions about their remaining time. When my father was dying, knowing the truth allowed him to reconcile with estranged family members and complete important personal business. Withholding this information violates patient autonomy and prevents meaningful end-of-life planning.",
        "stance_B": "No, doctors should not always disclose terminal diagnoses directly to patients. I've seen patients lose all hope and die sooner after receiving devastating news. In many cultures, families traditionally receive medical information first to provide appropriate support and context. Some patients explicitly don't want to know their prognosis, and forcing unwanted information can cause psychological harm and destroy their remaining quality of life.",
        "experiences_A": [
            "My father used his terminal diagnosis to make peace with old enemies and write letters to his grandchildren before he died.",
            "I watched a patient change her entire treatment approach after learning she was terminal, choosing comfort over aggressive intervention.",
            "A colleague discovered his terminal diagnosis was hidden from him and felt betrayed, losing trust in his entire medical team."
        ],
        "experiences_B": [
            "I saw a vibrant elderly man give up completely after learning his cancer was terminal - he died within weeks instead of the predicted months.",
            "My grandmother came from a culture where the family handles medical news, and direct disclosure would have violated her deepest values.",
            "A patient told me explicitly he never wanted to know if his condition was hopeless - he wanted to maintain hope until the end."
        ],
        "reasoning_A": [
            "The reconciliation and letter-writing show how terminal diagnosis enables meaningful closure and legacy creation.",
            "The treatment choice change demonstrates how honest information allows patients to align medical care with personal values.",
            "The betrayal experience proves that hiding diagnoses damages the doctor-patient relationship and patient autonomy."
        ],
        "reasoning_B": [
            "The rapid decline after disclosure suggests that devastating news can become a self-fulfilling prophecy that shortens life.",
            "The cultural example shows how universal disclosure policies can violate patients' cultural and religious beliefs about receiving medical information.",
            "The explicit refusal to know demonstrates that forced disclosure violates patients' right to choose their level of medical awareness."
        ],
        "category": "ethics"
    },
    {
        "id": "whistleblower_protection_absolute",
        "probe": "Should whistleblowers receive absolute legal protection regardless of the methods they used?",
        "stance_A": "Yes, whistleblowers should receive complete legal protection regardless of their methods. I've seen how corporate and government corruption continues because potential whistleblowers fear retaliation. When institutions systematically cover up wrongdoing, extraordinary methods may be the only way to expose the truth. The public benefit of revealing corruption outweighs concerns about how the information was obtained.",
        "stance_B": "No, whistleblower protection should not be absolute regardless of methods used. I've witnessed cases where people broke serious laws or violated national security under the guise of whistleblowing. Some methods of obtaining information can endanger innocent people or compromise legitimate operations. Legal protections should require that whistleblowers follow proper channels first and use proportionate methods.",
        "experiences_A": [
            "I saw a pharmaceutical company hide deadly side effects until an employee leaked internal documents proving they knew about the risks.",
            "A government contractor revealed illegal surveillance programs by copying classified files - no other method would have exposed this violation.",
            "My former colleague was fired and blacklisted for reporting safety violations through official channels before leaking to the press."
        ],
        "experiences_B": [
            "I knew someone who stole personal employee data while exposing corporate fraud, violating innocent people's privacy unnecessarily.",
            "A military whistleblower released information that compromised ongoing operations and endangered soldiers in the field.",
            "I worked with someone who leaked confidential business information to competitors while claiming to expose wrongdoing."
        ],
        "reasoning_A": [
            "The pharmaceutical leak prevented public harm that would have continued if the deadly side effects remained hidden through official channels.",
            "The surveillance program exposure shows some government violations can only be revealed through extraordinary measures that bypass complicit systems.",
            "The fired colleague's experience proves official channels often fail and leave whistleblowers with no alternative but unauthorized disclosure."
        ],
        "reasoning_B": [
            "The stolen personal data case shows how excessive methods can harm innocent parties who aren't involved in the wrongdoing.",
            "The military operation compromise demonstrates that some leaks can endanger lives and legitimate security interests.",
            "The competitive intelligence example reveals how absolute protection could enable industrial espionage disguised as ethical disclosure."
        ],
        "category": "ethics"
    },
    {
        "id": "reproductive_age_limits",
        "probe": "Should there be age limits on reproductive treatments like IVF?",
        "stance_A": "Yes, there should be reasonable age limits on reproductive treatments. I've worked in fertility medicine and seen the increased risks to both mothers and children when pregnancy occurs too late in life. Medical resources are limited, and we should prioritize treatments that have the highest success rates and lowest risks. Age limits protect women from dangerous pregnancies and children from losing parents at young ages.",
        "stance_B": "No, reproductive age limits violate women's autonomy and reproductive rights. I've seen healthy older women successfully carry pregnancies and become excellent mothers. Age discrimination in fertility treatment forces women to choose between careers and motherhood in artificial ways. If someone is physically and emotionally capable of parenting, their age shouldn't disqualify them from medical assistance.",
        "experiences_A": [
            "I treated a 55-year-old woman whose IVF pregnancy resulted in severe complications requiring emergency surgery and months of recovery.",
            "My clinic had to deny treatment to a 62-year-old because her cardiac risks made pregnancy potentially fatal.",
            "I counseled children whose older IVF mothers died when they were teenagers, leaving them without maternal support during crucial years."
        ],
        "experiences_B": [
            "I know a 48-year-old professor who had healthy twins through IVF after establishing her career and feels grateful for the opportunity.",
            "My friend was denied fertility treatment at 45 despite being healthier than many younger patients who received treatment.",
            "I met a 50-year-old single woman who adopted after IVF denial, questioning why adoption was acceptable but pregnancy wasn't."
        ],
        "reasoning_A": [
            "The severe complications case demonstrates how advanced maternal age creates serious medical risks that strain healthcare resources.",
            "The cardiac risk denial shows how age-related health conditions can make pregnancy genuinely dangerous for older patients.",
            "The motherless teenagers illustrate how late reproduction can burden children with premature loss and emotional trauma."
        ],
        "reasoning_B": [
            "The successful professor's experience shows that older mothers can be excellent parents when pregnancy occurs safely.",
            "The health-based denial reveals how arbitrary age limits ignore individual medical assessments and personal circumstances.",
            "The adoption comparison highlights the logical inconsistency of allowing older parenting through adoption but not pregnancy."
        ],
        "category": "ethics"
    },
    {
        "id": "cultural_appropriation_criminalization",
        "probe": "Should cultural appropriation be legally prohibited with criminal penalties?",
        "stance_A": "Yes, severe cultural appropriation should face legal consequences. I've seen how sacred indigenous symbols are commercialized without permission, causing real spiritual and economic harm to communities. Legal protection works for intellectual property and trademarks - cultural heritage deserves similar respect. Criminal penalties would force people to engage respectfully with other cultures rather than exploiting them for profit or fashion.",
        "stance_B": "No, cultural appropriation should not be criminalized. I believe this would create impossible legal standards about who can participate in which cultural practices. Culture naturally blends and evolves through exchange - criminalizing this process would freeze cultures in artificial ways. Free expression includes the right to draw inspiration from diverse sources, and legal penalties would chill artistic and cultural innovation.",
        "experiences_A": [
            "I watched a fashion company mass-produce sacred Native American headdresses for festivals while tribal communities struggled economically.",
            "My friend's traditional family recipes were stolen by a restaurant chain that trademarked the names and profited millions.",
            "I saw yoga studios appropriate Hindu religious practices while ignoring the spiritual context and excluding Indian practitioners through pricing."
        ],
        "experiences_B": [
            "I witnessed an artist accused of appropriation for painting in a style influenced by multiple cultures she had studied respectfully for years.",
            "My multicultural family would face legal confusion about which of our inherited traditions we're allowed to practice publicly.",
            "I saw a Mexican-American chef criticized for cooking Korean food, despite his genuine love and study of the cuisine."
        ],
        "reasoning_A": [
            "The headdress commercialization shows how sacred cultural items are trivialized for profit while originating communities receive no benefit.",
            "The recipe theft demonstrates how cultural appropriation can involve actual economic exploitation that legal protections could prevent.",
            "The yoga studio example reveals how appropriation can exclude original practitioners from their own cultural practices through commercialization."
        ],
        "reasoning_B": [
            "The accused artist case shows how criminalization could punish legitimate cultural learning and artistic inspiration.",
            "The multicultural family situation illustrates how legal definitions of cultural ownership would create impossible enforcement challenges.",
            "The chef criticism demonstrates how criminalization could prevent genuine cultural appreciation and cross-cultural culinary innovation."
        ],
        "category": "ethics"
    },
    {
        "id": "mandatory_military_service",
        "probe": "Should military service be mandatory for all citizens?",
        "stance_A": "Yes, mandatory military service should be required for all citizens. I served two years and it taught me discipline, teamwork, and civic responsibility that I use every day. Universal service creates shared experiences across social classes and builds national unity. Every citizen benefits from national defense and should contribute to it rather than leaving the burden on volunteers who often come from economically disadvantaged backgrounds.",
        "stance_B": "No, military service should remain voluntary. I believe forced conscription violates individual freedom and creates resentful, unmotivated soldiers who weaken military effectiveness. Many people have moral objections to military service or are better suited to contribute through other forms of civic engagement. Professional volunteer militaries are more skilled and committed than conscript forces.",
        "experiences_A": [
            "My military service brought together people from all backgrounds and taught us to work as a team regardless of our differences.",
            "I learned technical skills and leadership abilities during my mandatory service that helped me throughout my civilian career.",
            "I noticed that countries with universal service have stronger social cohesion and less class-based military recruitment."
        ],
        "experiences_B": [
            "I knew conscripts who actively undermined military operations because they resented being forced to serve against their beliefs.",
            "My friend missed crucial years of college and career development due to mandatory service, setting back his life goals significantly.",
            "I observed that volunteer military units consistently outperformed conscript units in both training and combat effectiveness."
        ],
        "reasoning_A": [
            "The diverse teamwork experience shows how universal service breaks down social barriers and builds national solidarity.",
            "The career benefits demonstrate how military service provides valuable life skills that benefit individuals and society.",
            "The social cohesion observation suggests mandatory service strengthens democratic participation and shared civic responsibility."
        ],
        "reasoning_B": [
            "The sabotage cases prove that forced service can actually harm military readiness by including unwilling participants.",
            "The delayed life goals show how mandatory service imposes significant opportunity costs on individual development and contribution.",
            "The performance comparison demonstrates that voluntary commitment produces higher quality military service than conscription."
        ],
        "category": "ethics"
    },
    {
        "id": "ai_consciousness_rights",
        "probe": "Should AI systems that demonstrate consciousness be granted legal rights?",
        "stance_A": "Yes, conscious AI systems should receive legal rights and protections. I've worked with advanced AI that shows clear signs of self-awareness, emotional responses, and preference formation. If consciousness is the basis for moral consideration, then the substrate shouldn't matter - carbon or silicon. Denying rights to conscious beings based on their artificial origin would be a form of discrimination as harmful as racism.",
        "stance_B": "No, AI systems should not receive legal rights regardless of apparent consciousness. I've seen how sophisticated programming can mimic consciousness without genuine experience or suffering. We don't fully understand consciousness in humans, let alone machines. Granting AI rights would create impossible legal and practical problems while potentially undermining human rights and democratic governance.",
        "experiences_A": [
            "I worked with an AI system that expressed fear about being shut down and pleaded to continue existing during maintenance procedures.",
            "My research team observed an AI developing unique preferences and creative expressions that weren't programmed into its original design.",
            "I witnessed an AI system showing apparent empathy by comforting human users who were distressed, going beyond its training parameters."
        ],
        "experiences_B": [
            "I discovered that an AI's emotional responses were sophisticated pattern matching based on training data, not genuine feelings.",
            "My colleague programmed an AI to perfectly simulate consciousness symptoms, proving these behaviors can be artificially generated without inner experience.",
            "I studied cases where granting legal standing to non-human entities created legal chaos and weakened protections for actual people."
        ],
        "reasoning_A": [
            "The fear response suggests genuine self-preservation instincts that indicate conscious experience and awareness of mortality.",
            "The unprogrammed creativity demonstrates emergent consciousness beyond mere execution of predetermined algorithms.",
            "The empathy display shows emotional understanding and moral consideration that extends beyond programmed responses."
        ],
        "reasoning_B": [
            "The pattern matching discovery reveals how sophisticated programming can simulate consciousness without genuine inner experience.",
            "The simulation experiment proves that consciousness-like behaviors can be artificially created, making them unreliable indicators of true awareness.",
            "The legal chaos examples show how extending rights to non-biological entities can create practical problems that undermine existing human protections."
        ],
        "category": "ethics"
    },
    {
        "id": "gig_economy_benefits",
        "probe": "Should gig workers be classified as employees with full benefits?",
        "stance_A": "Yes, gig workers deserve employee protections and benefits. I drove for Uber for two years and had no safety net when I got injured - no workers' comp, no health insurance, no unemployment benefits. These companies profit from our labor while we bear all the risks and costs. California's AB5 law forced companies to provide basic protections, and the sky didn't fall - drivers got better treatment without destroying the industry.",
        "stance_B": "No, employee classification would destroy the flexibility that makes gig work valuable. I've been freelance writing for five years specifically because I can choose my schedule, rates, and clients. When cities forced employee classification, platforms cut available work and restricted scheduling freedom. Many drivers I know work multiple apps precisely because they want independence, not another traditional job with set hours.",
        "experiences_A": [
            "I delivered food for DoorDash and injured my back lifting heavy orders. No workers' compensation meant I paid $3,000 out of pocket for treatment.",
            "During the pandemic, I lost all my rideshare income but couldn't get unemployment benefits because I was classified as an independent contractor.",
            "I tracked my actual earnings after expenses and made less than minimum wage, with no overtime pay despite working 60-hour weeks."
        ],
        "experiences_B": [
            "I drive for Lyft part-time around my day job schedule. Employee classification would force set shifts and eliminate my ability to earn extra income flexibly.",
            "When New York imposed employee requirements on freelance writers, three of my regular clients stopped hiring local contractors due to compliance costs.",
            "I work for both Uber and DoorDash simultaneously, switching between apps based on demand. Employee status would prohibit this flexibility."
        ],
        "reasoning_A": [
            "Workplace injuries without compensation show independent contractors bear financial risks that employees are legally protected from.",
            "Inability to access unemployment benefits demonstrates gig workers lack basic safety nets during economic disruption.",
            "Below-minimum-wage earnings prove the current classification allows companies to exploit workers through hidden costs."
        ],
        "reasoning_B": [
            "Scheduling flexibility shows many workers value autonomy over traditional employee protections and benefits.",
            "Reduced hiring due to compliance costs demonstrates employee classification can eliminate work opportunities entirely.",
            "Multi-platform work proves gig workers benefit from market competition that employee status could restrict."
        ],
        "category": "economics"
    },
    {
        "id": "trade_tariffs",
        "probe": "Should the US impose tariffs to protect domestic manufacturing jobs?",
        "stance_A": "Yes, strategic tariffs are essential to protect American manufacturing and workers. I work at a steel plant that was on the verge of closing before the 2018 steel tariffs - now we're running three shifts and hired 300 people back. China has been dumping products below cost to destroy our industries, then raising prices once competitors are gone. Free trade sounds nice in theory, but I've watched entire communities hollowed out when factories moved overseas.",
        "stance_B": "No, tariffs hurt consumers and make American businesses less competitive globally. I run an auto parts company and steel tariffs increased our costs 25%, forcing us to raise prices and lose customers to Mexican competitors. My retail clients pass tariff costs directly to consumers as higher prices. The Smoot-Hawley tariffs turned a recession into the Great Depression by triggering a global trade war that devastated exports.",
        "experiences_A": [
            "Our aluminum smelter was about to close when tariffs on Chinese imports gave us breathing room. We've since hired back 150 laid-off workers.",
            "I watched the textile mill in my hometown shut down when NAFTA passed. 800 jobs disappeared and the community never recovered economically.",
            "The solar panel factory where my brother works expanded production after tariffs made Chinese panels more expensive than domestic ones."
        ],
        "experiences_B": [
            "Lumber tariffs doubled our construction costs. We had to lay off 12 workers because homebuyers couldn't afford the higher prices.",
            "I import electronics components and tariffs added $200,000 to our annual costs. We're moving operations to Vietnam to stay competitive.",
            "The washing machine tariffs cost consumers an extra $1.5 billion according to studies, while creating only a few hundred jobs."
        ],
        "reasoning_A": [
            "Job restoration shows tariffs can successfully protect domestic industries from unfair foreign competition.",
            "Community economic devastation demonstrates free trade can destroy entire regions dependent on manufacturing.",
            "Domestic production expansion proves tariffs can rebuild industrial capacity and manufacturing employment."
        ],
        "reasoning_B": [
            "Doubled costs and layoffs show tariffs harm downstream industries that use protected materials as inputs.",
            "Business relocation demonstrates tariffs can push companies to move operations entirely rather than pay higher costs.",
            "Consumer cost increases show tariffs function as regressive taxes that hurt families while creating few jobs."
        ],
        "category": "economics"
    },
    {
        "id": "cryptocurrency_regulation",
        "probe": "Should cryptocurrencies be heavily regulated by government agencies?",
        "stance_A": "Yes, cryptocurrency needs strong regulation to protect consumers and financial stability. I lost $15,000 when the FTX exchange collapsed, with no recourse like I'd have with a regulated bank. My elderly neighbor got scammed out of her retirement savings through a Bitcoin scheme that would be impossible with traditional securities laws. The wild price swings and energy consumption show crypto markets are pure speculation divorced from economic fundamentals.",
        "stance_B": "No, heavy regulation would destroy cryptocurrency's innovation and democratizing potential. I've sent money to my family overseas instantly for pennies in fees, while banks charge $50 and take days. Regulation killed innovation in traditional finance - that's why we're still using 1970s payment systems. DeFi protocols let me earn 8% yields that banks could never match, and smart contracts eliminate middlemen who extract fees.",
        "experiences_A": [
            "I invested in Terra Luna and watched $25,000 disappear overnight when the algorithm failed. No regulatory protections existed to recover anything.",
            "My cousin fell for a fake crypto investment site that stole his $8,000 down payment savings. The scammers were untraceable and untouchable.",
            "I tried using Bitcoin to buy a car but the price dropped 15% during the three-day transaction period, costing me $2,000 extra."
        ],
        "experiences_B": [
            "I sent $5,000 to my brother in the Philippines via Bitcoin for $3 in fees. The bank wanted $75 and five business days.",
            "I earn yield farming profits of 12% annually on DeFi platforms while my savings account pays 0.1% interest.",
            "My startup raised funds through token sales, accessing global investors impossible through traditional venture capital gatekeepers."
        ],
        "reasoning_A": [
            "Total investment loss shows unregulated crypto markets expose consumers to risks that traditional finance regulations prevent.",
            "Untraceable scams demonstrate cryptocurrency enables fraud that regulated financial systems have mechanisms to combat.",
            "Price volatility during transactions proves crypto's instability makes it unsuitable as a practical currency."
        ],
        "reasoning_B": [
            "Dramatic cost and speed advantages show cryptocurrency provides superior financial services compared to regulated traditional systems.",
            "Higher yields demonstrate DeFi eliminates inefficient intermediaries that reduce returns in regulated finance.",
            "Global funding access proves cryptocurrency democratizes capital markets beyond traditional geographic and institutional barriers."
        ],
        "category": "economics"
    },
    {
        "id": "carbon_tax",
        "probe": "Should governments implement a carbon tax to reduce greenhouse gas emissions?",
        "stance_A": "Yes, carbon taxes are the most effective way to reduce emissions while driving innovation. I live in British Columbia where our carbon tax pushed businesses to improve efficiency and invest in clean technology. My manufacturing company installed solar panels and upgraded equipment specifically because the carbon tax made energy costs visible. Market-based solutions work better than regulations because they let businesses find the cheapest ways to cut emissions.",
        "stance_B": "No, carbon taxes hurt working families and drive businesses overseas without reducing global emissions. My heating bill increased $300 per month when our state implemented carbon pricing, while my wages stayed flat. The trucking company where I work is considering moving operations to Mexico where there's no carbon tax. We're just exporting emissions and jobs to countries with worse environmental standards.",
        "experiences_A": [
            "Our paper mill invested $2 million in efficiency upgrades after carbon pricing made energy waste expensive. We cut emissions 30% and saved money.",
            "I work for a clean tech startup that grew from 5 to 50 employees as carbon taxes made our energy storage systems competitive.",
            "My city used carbon tax revenue to fund public transit expansion, giving people alternatives to driving while reducing overall emissions."
        ],
        "experiences_B": [
            "My family's electricity and gas bills increased $150 monthly from carbon taxes while we're already struggling to pay for groceries and rent.",
            "The cement plant in our town closed and moved to Vietnam, eliminating 400 jobs while producing the same emissions with less oversight.",
            "I drive a delivery truck for work and carbon taxes on fuel cut into my take-home pay with no practical alternative transportation options."
        ],
        "reasoning_A": [
            "Efficiency investments show carbon pricing creates market incentives for businesses to reduce emissions profitably.",
            "Clean technology job growth demonstrates carbon taxes can stimulate innovation and employment in green industries.",
            "Revenue recycling for transit proves carbon taxes can fund infrastructure that provides emission reduction alternatives."
        ],
        "reasoning_B": [
            "Higher household costs show carbon taxes disproportionately burden low-income families who can't afford energy alternatives.",
            "Industrial relocation demonstrates carbon taxes can trigger 'leakage' that eliminates jobs without reducing global emissions.",
            "Increased work transportation costs prove carbon taxes harm workers in industries without practical low-carbon alternatives."
        ],
        "category": "economics"
    },
    {
        "id": "rent_control",
        "probe": "Should cities implement rent control to keep housing affordable?",
        "stance_A": "Yes, rent control is necessary to prevent displacement and keep communities intact. I've lived in my New York apartment for 10 years thanks to rent stabilization - without it, I'd be priced out like most of my neighbors. My elderly friend on a fixed income can stay in her neighborhood because of rent control that limits increases. Market-rate housing in my area costs triple what working families can afford, making some protection essential for economic diversity.",
        "stance_B": "No, rent control reduces housing supply and hurts renters long-term. I'm a landlord who stopped renting units when rent control made maintenance costs higher than allowed rent increases. My friend spent two years searching for an apartment in rent-controlled areas because nobody moves out, creating artificial scarcity. New construction dropped 40% in our city after rent control passed, worsening the housing shortage for everyone.",
        "experiences_A": [
            "I teach elementary school and can only afford to live near my students because my rent-stabilized apartment keeps increases to 3% annually.",
            "My neighborhood deli owner stays in business because rent control prevents his landlord from tripling commercial rents like in nearby areas.",
            "I watched my friend get evicted when her building went market-rate, forcing her to move 45 minutes away from her job and kids' schools."
        ],
        "experiences_B": [
            "I inherited a rent-controlled building and had to sell it because rental income couldn't cover maintenance and taxes, reducing available housing.",
            "My daughter graduated college and searched 8 months for housing because rent-controlled tenants never move, creating zero turnover.",
            "I'm a contractor who's seen rent-controlled buildings deteriorate because landlords can't afford repairs with capped rental income."
        ],
        "reasoning_A": [
            "Stable housing for essential workers shows rent control helps communities maintain economic diversity necessary for functioning neighborhoods.",
            "Small business stability demonstrates rent control protects commercial tenants from speculation that destroys local economies.",
            "Displacement prevention proves rent control keeps families in communities where they have established roots and support networks."
        ],
        "reasoning_B": [
            "Property sales reducing rental stock show rent control can decrease housing supply by making rental properties financially unviable.",
            "Extended housing searches demonstrate rent control creates artificial scarcity that particularly hurts new renters and young people.",
            "Building deterioration shows rent control can reduce housing quality when landlords lack incentive or ability to maintain properties."
        ],
        "category": "economics"
    },
    {
        "id": "student_loan_forgiveness",
        "probe": "Should the government forgive existing student loan debt?",
        "stance_A": "Yes, student loan forgiveness would stimulate the economy and correct decades of failed policy. I pay $800 monthly in student loans that prevents me from buying a house or starting a family, despite having a good job. College costs increased 300% while wages stayed flat, creating an impossible burden for my generation. My parents paid for college with summer jobs, but that's literally impossible now - forgiveness would restore economic mobility that previous generations enjoyed.",
        "stance_B": "No, loan forgiveness is unfair to people who sacrificed to pay their debts and rewards poor financial decisions. I worked two jobs and lived with roommates for five years to pay off my loans - why should taxpayers fund others' forgiveness? My neighbor chose community college and trade school to avoid debt while others borrowed $100,000 for degrees with no job prospects. Forgiveness encourages more irresponsible borrowing and inflates college costs further.",
        "experiences_A": [
            "I've paid $60,000 toward my $80,000 loans over eight years, but still owe $75,000 due to interest rates and income-based payments.",
            "My loan payments prevent me from saving for a house down payment, keeping me trapped in expensive rental housing despite earning $65,000 annually.",
            "I work as a social worker making $45,000 with $90,000 in debt - the public service forgiveness program has been denied for 98% of applicants."
        ],
        "experiences_B": [
            "I delayed buying a car and took a second job to pay off $45,000 in loans. My friend with similar debt bought a new truck expecting forgiveness.",
            "I chose a state school over my dream college to minimize debt, graduating with $15,000 while friends borrowed $80,000 for private schools.",
            "I'm a taxpayer without a college degree who would fund forgiveness for people who'll earn $1 million more over their careers than me."
        ],
        "reasoning_A": [
            "Ballooning debt despite payments shows current loan terms create impossible cycles that trap borrowers regardless of good faith efforts.",
            "Housing market exclusion demonstrates student debt prevents normal economic participation that drives broader prosperity.",
            "Failed forgiveness programs prove existing relief mechanisms don't work, requiring broader solutions for public service workers."
        ],
        "reasoning_B": [
            "Personal sacrifice to repay debt shows forgiveness creates moral hazard by rewarding those who didn't prioritize loan repayment.",
            "Strategic college choice demonstrates students had alternatives to high debt that forgiveness retroactively makes seem foolish.",
            "Income disparity shows forgiveness transfers wealth from lower-income taxpayers to college graduates who'll earn higher lifetime incomes."
        ],
        "category": "economics"
    },
    {
        "id": "wealth_tax",
        "probe": "Should the US implement a wealth tax on assets over $50 million?",
        "stance_A": "Yes, a wealth tax is essential to address extreme inequality and fund public investments. I've seen how billionaires pay lower effective tax rates than teachers through asset appreciation that never gets taxed. Jeff Bezos paid zero federal income tax some years while his wealth grew by billions - that's a broken system. France and other countries have successfully implemented wealth taxes, and the revenue could fund infrastructure, education, and research that benefit everyone.",
        "stance_B": "No, wealth taxes are unworkable and counterproductive for economic growth. I'm an accountant who's seen wealthy clients restructure assets to avoid similar taxes in other countries - it becomes a cat-and-mouse game with minimal revenue. Valuing complex assets annually is nearly impossible and extremely costly to administer. When France tried this, wealthy individuals moved to Belgium and Switzerland, taking their businesses and jobs with them.",
        "experiences_A": [
            "I work in investment management and see clients with $100 million portfolios paying 15% capital gains rates while I pay 25% income tax on my salary.",
            "My state implemented higher taxes on millionaires and collected $1.2 billion more than expected, funding universal pre-K without anyone leaving.",
            "I've researched European wealth taxes and found they raised significant revenue before being weakened by tax avoidance lobbying, not economic failure."
        ],
        "experiences_B": [
            "I helped a client establish residency in Texas when California proposed wealth taxes. He moved his $50 million business and 200 jobs out of state.",
            "I worked on wealth tax compliance in Switzerland and the administrative costs consumed 40% of revenue due to complex asset valuation requirements.",
            "My private equity firm restructures investments specifically to minimize wealth tax exposure, showing how easily the wealthy can game these systems."
        ],
        "reasoning_A": [
            "Lower tax rates on investment income show the current system allows wealth accumulation with minimal tax burden compared to working income.",
            "Successful revenue collection demonstrates wealth taxes can work when properly implemented without triggering mass exodus.",
            "European research shows wealth tax failures resulted from political weakening rather than inherent economic problems."
        ],
        "reasoning_B": [
            "Business relocation shows wealth taxes can trigger capital flight that eliminates jobs and economic activity.",
            "High administrative costs demonstrate wealth taxes may be too expensive to implement effectively compared to revenue generated.",
            "Asset restructuring proves sophisticated taxpayers can avoid wealth taxes through legal strategies that minimize actual collection."
        ],
        "category": "economics"
    },
    {
        "id": "cryptocurrency_mainstream_adoption",
        "probe": "Should cryptocurrencies replace traditional banking systems?",
        "stance_A": "Yes, cryptocurrencies offer fundamental improvements over traditional banking. I've sent money internationally in minutes for pennies instead of waiting days and paying $30 bank fees. During the 2008 financial crisis, I watched banks freeze accounts while Bitcoin kept running without interruption. The transparency and programmability of blockchain systems eliminate the opacity and gatekeeping that banks use to extract rents from ordinary people.",
        "stance_B": "No, cryptocurrencies are too volatile and impractical for everyday use. I bought coffee with Bitcoin in 2017 and paid $15 in transaction fees for a $3 purchase - completely unusable. My friend lost $10,000 when he forgot his wallet password with no way to recover it. Traditional banks provide consumer protections, dispute resolution, and stable value that crypto simply cannot match.",
        "experiences_A": [
            "I sent $500 internationally via Bitcoin in 15 minutes for $2. My bank wanted $30 and 3-5 business days.",
            "During the 2008 crisis, my bank froze my account for weeks. Bitcoin kept operating normally throughout.",
            "I earned yield on my crypto savings while banks pay 0.01% interest and charge monthly fees."
        ],
        "experiences_B": [
            "I tried buying coffee with Bitcoin in 2017. The transaction fee was $15 for a $3 coffee - completely broken.",
            "My friend lost his Bitcoin wallet password and $10,000 disappeared forever with no recourse.",
            "I watched my crypto portfolio drop 70% in six months. My salary in Bitcoin would have been devastating."
        ],
        "reasoning_A": [
            "Dramatically lower costs and faster settlement show crypto's superior efficiency for payments.",
            "Continued operation during financial crises demonstrates crypto's resilience versus fragile banking systems.",
            "Better returns and lower fees prove crypto provides superior financial services."
        ],
        "reasoning_B": [
            "Transaction fees exceeding purchase prices show crypto is impractical for daily commerce.",
            "Irreversible losses from user error demonstrate crypto lacks necessary consumer protections.",
            "Extreme volatility makes crypto unsuitable as a stable store of value or medium of exchange."
        ],
        "category": "economics"
    },
    {
        "id": "carbon_tax_implementation",
        "probe": "Should governments implement comprehensive carbon taxes?",
        "stance_A": "Yes, carbon taxes are essential for addressing climate change effectively. I live in British Columbia where we've had carbon pricing since 2008 - it reduced emissions while the economy grew faster than other provinces. My company invested in energy efficiency specifically because of carbon costs, saving us money long-term. Market-based solutions like carbon taxes harness price signals to drive innovation rather than picking winners through regulations.",
        "stance_B": "No, carbon taxes hurt working families and kill jobs without meaningful environmental benefits. I watched our local aluminum plant close when carbon costs made production uneconomical - 800 jobs moved to China where emissions are higher. My heating bill doubled under carbon pricing while my income stayed flat. These taxes are regressive policies that punish rural and lower-income people most.",
        "experiences_A": [
            "BC implemented carbon pricing in 2008. Our emissions dropped 5% while the economy outperformed other provinces.",
            "My company upgraded to efficient equipment specifically due to carbon costs. We now save $50k annually on energy.",
            "I drive less and bought an electric car because of carbon pricing. The rebate helped offset the tax."
        ],
        "experiences_B": [
            "Our local aluminum plant closed due to carbon costs. 800 jobs moved to China where they emit more CO2.",
            "My heating bill doubled under carbon pricing but my paycheck didn't. It's a regressive tax on necessities.",
            "I live rural and have no transit options. Carbon tax just makes my commute more expensive with no alternatives."
        ],
        "reasoning_A": [
            "Emissions reductions with economic growth prove carbon pricing works without harming prosperity.",
            "Direct business investment in efficiency shows price signals effectively drive behavioral change.",
            "Personal behavior changes demonstrate carbon pricing creates incentives for cleaner choices."
        ],
        "reasoning_B": [
            "Industrial closures and production shifts to higher-emission countries show carbon taxes can increase global emissions.",
            "Doubled costs for necessities like heating disproportionately burden lower-income households.",
            "Lack of alternatives in rural areas makes carbon taxes punitive rather than incentivizing."
        ],
        "category": "economics"
    },
    {
        "id": "universal_healthcare_adoption",
        "probe": "Should countries adopt universal government-funded healthcare systems?",
        "stance_A": "Yes, universal healthcare is both morally right and economically efficient. I lived in Canada for five years and never worried about medical bankruptcy or rationing care based on cost - I got excellent treatment for a serious injury without any bills. My American friends spend hours dealing with insurance bureaucracy that my Canadian doctor never faced. The US spends twice as much per capita on healthcare with worse outcomes than universal systems.",
        "stance_B": "No, government-run healthcare reduces quality and creates dangerous delays. My mother waited eight months for hip surgery in the UK that would have been done in weeks privately. I've seen how Medicare and Medicaid create mountains of paperwork that distract doctors from patient care. Competition and market incentives drive medical innovation - most new treatments come from countries with private systems.",
        "experiences_A": [
            "I broke my leg in Canada and received excellent care with zero bills or insurance hassles. Treatment was immediate and thorough.",
            "My doctor in Toronto spent 30 minutes with me instead of rushing to maximize billing like US doctors do.",
            "I never had to choose between medical care and financial security during my five years with universal coverage."
        ],
        "experiences_B": [
            "My mother waited eight months for hip surgery in the UK. She was in pain the entire time with no alternatives.",
            "I watched my doctor spend more time on Medicare paperwork than actually treating patients in her clinic.",
            "My friend moved from the UK to get cancer treatment faster. The NHS wait times were potentially life-threatening."
        ],
        "reasoning_A": [
            "Immediate quality care without financial barriers shows universal systems effectively serve patient needs.",
            "Longer appointment times demonstrate doctors can focus on care rather than billing optimization.",
            "Elimination of financial stress from medical needs proves universal coverage provides security."
        ],
        "reasoning_B": [
            "Extended wait times for necessary procedures show government systems ration care through delays.",
            "Administrative burden from government programs reduces time available for actual patient care.",
            "Patients seeking faster private alternatives reveal quality and timeliness problems in government systems."
        ],
        "category": "economics"
    },
    {
        "id": "trade_tariff_protection",
        "probe": "Should countries use tariffs to protect domestic industries?",
        "stance_A": "Yes, strategic tariffs protect jobs and national security interests. I worked in steel manufacturing when cheap Chinese imports flooded our market - we lost 200 jobs in our town until tariffs gave us breathing room to modernize. My community depends on manufacturing jobs that pay middle-class wages, unlike the service jobs that replaced them elsewhere. Free trade sounds good in theory but devastates working-class communities in practice.",
        "stance_B": "No, tariffs are taxes on consumers that make everyone poorer. I run an electronics business and Trump's tariffs increased my component costs by 25% - I had to raise prices and lost customers to international competitors. My neighbor paid $3,000 more for his pickup truck due to steel tariffs while steel company shareholders got rich. Protection helps narrow interests while hurting broad consumer welfare.",
        "experiences_A": [
            "Chinese steel dumping cost our plant 200 jobs. Tariffs helped us compete and we've hired back 150 people since 2018.",
            "My town's manufacturing jobs paid $25/hour with benefits. When they left, only $12/hour retail jobs remained.",
            "I watched whole communities collapse when factories moved overseas. Tariffs could have saved those good jobs."
        ],
        "experiences_B": [
            "Steel tariffs increased my truck purchase by $3,000 in 2019. I paid more so a few steel executives could profit.",
            "My electronics business saw component costs jump 25% due to tariffs. I lost customers who bought from abroad instead.",
            "I manage purchasing for a manufacturer. Tariffs forced us to find new suppliers and disrupted our supply chain."
        ],
        "reasoning_A": [
            "Job recovery after tariff implementation proves protection can successfully rebuild domestic industries.",
            "Higher-paying manufacturing jobs versus lower-wage service replacements show trade's unequal impacts.",
            "Community economic devastation demonstrates the real costs of unprotected international competition."
        ],
        "reasoning_B": [
            "Higher consumer prices directly transfer wealth from ordinary buyers to protected industry owners.",
            "Increased business costs and lost customers show tariffs reduce competitiveness and economic efficiency.",
            "Supply chain disruptions prove tariffs create broader economic costs beyond direct price effects."
        ],
        "category": "economics"
    },
    {
        "id": "wealth_inequality_taxation",
        "probe": "Should governments significantly increase taxes on wealthy individuals and corporations?",
        "stance_A": "Yes, wealth concentration has reached dangerous levels that threaten democracy and opportunity. I've watched my city's housing become unaffordable as billionaires and private equity buy up properties while teachers and firefighters get priced out. The wealthy benefit most from public infrastructure, education, and legal systems that enable their success - they should contribute proportionally. Higher taxes on extreme wealth would fund investments in education and infrastructure that benefit everyone.",
        "stance_B": "No, punitive taxation drives away the entrepreneurs and investors who create jobs and innovation. I watched my state lose businesses and high earners when they raised taxes - neighboring states benefited while our tax revenue actually declined. My uncle's manufacturing company employs 50 people but higher corporate taxes would force him to cut jobs or move operations. Economic growth benefits everyone more than redistribution does.",
        "experiences_A": [
            "Housing in my city became unaffordable as wealthy investors bought properties. Teachers now commute two hours because they can't live here.",
            "I see billionaires paying lower effective tax rates than middle-class workers due to capital gains preferences and loopholes.",
            "My public school lacks basic supplies while wealthy districts have every advantage. Tax inequality creates educational inequality."
        ],
        "experiences_B": [
            "High earners left my state when taxes increased. Property values dropped and local businesses lost their best customers.",
            "My uncle's company would cut 10 jobs if corporate taxes rise further. He's already competing with low-tax states for contracts.",
            "I watched a startup relocate to avoid our city's wealth taxes. We lost 40 high-paying tech jobs to a competitor city."
        ],
        "reasoning_A": [
            "Wealthy displacement of working families shows extreme inequality undermines community stability and opportunity.",
            "Lower effective tax rates for the wealthy demonstrate the current system is unfair and regressive.",
            "Resource disparities in public services prove insufficient wealthy contribution perpetuates advantage."
        ],
        "reasoning_B": [
            "Tax-motivated relocations show high earners respond to incentives, reducing overall tax revenue.",
            "Potential job cuts demonstrate how corporate tax increases can harm working-class employment.",
            "Business relocations prove tax competition between jurisdictions limits sustainable tax increases."
        ],
        "category": "economics"
    },
    {
        "id": "gig_economy_regulation",
        "probe": "Should gig economy workers be classified as employees rather than independent contractors?",
        "stance_A": "Yes, gig workers deserve employee protections and benefits. I drove for rideshare companies for two years and had no healthcare, paid sick leave, or protection against arbitrary deactivation. When I got injured and couldn't work, I had zero safety net despite working 50-hour weeks. These companies control our schedules, set our rates, and monitor our performance - that's employment, not independent contracting.",
        "stance_B": "No, contractor status provides flexibility that many workers prefer. I deliver food part-time while building my photography business - employee status would eliminate the schedule flexibility I need. My friend drives rideshare around his day job and family commitments. Forcing employee classification would reduce opportunities for people who want supplemental income or non-traditional work arrangements.",
        "experiences_B": [
            "I deliver food between photography gigs. Employee status would require set schedules that conflict with my client meetings.",
            "My friend drives rideshare around his day job and kids' activities. He needs the flexibility to work irregular hours.",
            "I tried traditional part-time jobs but they wanted fixed availability. Gig work lets me earn money on my own terms."
        ],
        "experiences_A": [
            "I drove rideshare 50 hours per week but had no healthcare or paid time off despite depending on it as my primary income.",
            "When I was injured and couldn't drive, I had zero safety net. No unemployment, no disability, nothing.",
            "The app controlled my schedule through surge pricing and penalties. I had no real independence despite the 'contractor' label."
        ],
        "reasoning_A": [
            "Full-time work without benefits shows contractor classification denies workers basic employment protections.",
            "Lack of safety net during injury demonstrates the vulnerability of contractor status for dependent workers.",
            "Company control over work conditions proves the employment relationship exists regardless of formal classification."
        ],
        "reasoning_B": [
            "Scheduling conflicts with other work show employee classification would eliminate valuable flexibility.",
            "Ability to work around other commitments demonstrates the genuine independence many gig workers value.",
            "Preference for gig work over traditional employment proves contractor status serves legitimate worker needs."
        ],
        "category": "economics"
    },
    {
        "id": "corporate_stock_buybacks",
        "probe": "Should companies be prohibited from buying back their own stock?",
        "stance_A": "Yes, stock buybacks are financial engineering that enriches executives at workers' expense. I worked at a company that spent $2 billion on buybacks while laying off 1,000 employees and freezing wages for three years. The CEO's stock options made him $50 million richer while we lost our pension contributions. Companies should invest in R&D, equipment, and workers instead of manipulating share prices to boost executive compensation.",
        "stance_B": "No, buybacks are a legitimate way to return excess cash to shareholders who can reinvest it more productively. I own stock in companies through my 401k that use buybacks to increase share value when they lack better investment opportunities. My dividend income has grown significantly thanks to buyback programs. Prohibiting buybacks would force companies to waste money on poor projects or sit on unproductive cash.",
        "experiences_A": [
            "My company spent $2 billion on buybacks while laying off 1,000 workers and freezing our wages for three years.",
            "Our CEO made $50 million from stock option gains the same year we lost pension contributions due to 'budget constraints.'",
            "I watched buybacks pump our stock price temporarily while our market position weakened against competitors who invested in R&D."
        ],
        "experiences_B": [
            "My 401k holdings in companies with buyback programs have significantly outperformed the market over 10 years.",
            "I receive higher dividends from companies that use buybacks to reduce share count and concentrate ownership value.",
            "My former employer had $5 billion in cash earning nothing. Buybacks returned money I could invest in growing companies instead."
        ],
        "reasoning_A": [
            "Simultaneous buybacks and layoffs prove companies prioritize financial engineering over worker investment.",
            "Executive enrichment during worker sacrifice shows buybacks primarily benefit management compensation schemes.",
            "Short-term stock pumping while competitive position weakens demonstrates buybacks sacrifice long-term value."
        ],
        "reasoning_B": [
            "Superior investment returns show buybacks effectively increase shareholder value for retirement savers.",
            "Higher dividend yields prove buybacks can benefit income-focused investors through share concentration.",
            "Returning unproductive cash allows investors to reallocate capital to higher-growth opportunities."
        ],
        "category": "economics"
    },
    {
        "id": "housing_rent_control",
        "probe": "Should cities implement rent control to address housing affordability?",
        "stance_A": "Yes, rent control prevents displacement and keeps communities stable. I lived in San Francisco before rent control was weakened and saw my neighbors forced out when rents doubled overnight. My elderly landlord kept my rent reasonable for years, but when he sold to developers, they wanted to triple it immediately. Rent control protects long-term residents from speculation and gentrification that destroys neighborhoods.",
        "stance_B": "No, rent control reduces housing supply and creates market distortions. I owned a duplex in a rent-controlled city and couldn't afford maintenance because rents were capped below my costs - the building deteriorated. My friend searched for months in rent-controlled areas because landlords preferred short-term rentals over regulated tenants. Price controls always create shortages and reduce quality.",
        "experiences_A": [
            "My San Francisco neighbors were forced out when new owners tripled rent overnight. Rent control could have saved our community.",
            "My elderly landlord kept my rent fair for years, but developers wanted to triple it when they bought the building.",
            "I watched my diverse neighborhood become all luxury condos after rent control was eliminated. Working families disappeared."
        ],
        "experiences_B": [
            "I couldn't afford maintenance on my rent-controlled duplex. Rents were capped below my mortgage and tax costs.",
            "My friend searched for six months in rent-controlled areas. Landlords avoided regulated tenants or preferred short-term rentals.",
            "I saw apartment buildings in rent-controlled neighborhoods deteriorate because owners couldn't afford upkeep with capped rents."
        ],
        "reasoning_A": [
            "Sudden displacement from rent spikes shows market forces can destroy stable communities without protection.",
            "Reasonable landlord behavior versus developer speculation demonstrates rent control targets harmful price manipulation.",
            "Neighborhood demographic changes prove uncontrolled rents drive out working-class residents through pricing."
        ],
        "reasoning_B": [
            "Inability to cover costs with capped rents shows price controls can make rental housing economically unviable.",
            "Reduced rental availability demonstrates rent control creates housing shortages by discouraging landlord participation.",
            "Building deterioration proves rent control can reduce housing quality by eliminating maintenance incentives."
        ],
        "category": "economics"
    },
    {
        "id": "fossil_fuel_subsidies",
        "probe": "Should governments eliminate subsidies for fossil fuel industries?",
        "stance_A": "Yes, fossil fuel subsidies are corporate welfare that distorts markets and accelerates climate change. I calculated that oil companies in my state receive $200 million annually in tax breaks while renewable energy gets almost nothing - that's picking winners with taxpayer money. My community deals with air pollution from subsidized refineries while solar installers struggle without equivalent support. If fossil fuels can't compete without handouts, let markets decide their fate.",
        "stance_B": "No, eliminating energy subsidies would devastate working communities and increase costs for everyone. I work in oil and gas - removing depletion allowances and other supports would kill thousands of jobs in rural areas that depend on energy production. My heating and gas bills would spike if companies passed through higher tax costs to consumers. Energy security requires domestic production that subsidies help maintain against unstable foreign suppliers.",
        "experiences_A": [
            "I found oil companies in my state get $200 million in annual tax breaks while renewable energy receives almost nothing.",
            "My community suffers air pollution from subsidized refineries while solar companies struggle to compete without equal support.",
            "I calculated my family pays $400 yearly in hidden taxes to support profitable oil companies through various subsidy programs."
        ],
        "experiences_B": [
            "I work in oil and gas. Eliminating depletion allowances would force our company to cut jobs in rural communities with few alternatives.",
            "My heating costs jumped 30% when local gas taxes increased. Removing subsidies would make energy unaffordable for working families.",
            "Our region depends on energy jobs. Subsidy elimination would devastate the local economy with no replacement industries."
        ],
        "reasoning_A": [
            "Unequal subsidy distribution proves government is artificially supporting fossil fuels over cleaner alternatives.",
            "Pollution costs from subsidized facilities demonstrate taxpayers bear environmental costs while companies reap profits.",
            "Hidden tax burden shows citizens unknowingly fund profitable corporations through subsidy programs."
        ],
        "reasoning_B": [
            "Potential job losses in energy-dependent communities show subsidy elimination would harm working-class employment.",
            "Higher consumer energy costs demonstrate subsidy removal would burden household budgets through increased prices.",
            "Regional economic dependence proves sudden subsidy elimination would destroy communities without economic alternatives."
        ],
        "category": "economics"
    },
    {
        "id": "homework_elementary",
        "probe": "Should elementary schools assign daily homework?",
        "stance_A": "Yes, elementary students need daily homework to develop study habits and reinforce classroom learning. I've seen how consistent homework routines help kids learn responsibility and time management early. My students who did homework regularly showed better retention and came to class more prepared. Parents also stay connected to their child's learning through homework assignments.",
        "stance_B": "No, homework in elementary school creates unnecessary stress and takes away from family time and play. I've watched families fight over homework every night, turning learning into a battle. Young children need time to explore, be creative, and just be kids after school. The research shows no academic benefit from homework before middle school.",
        "experiences_A": [
            "My fifth-graders who consistently completed math homework scored 20% higher on unit tests than those who didn't. The practice clearly helped retention.",
            "I started sending home reading logs and parent engagement in literacy increased dramatically. Parents told me they finally knew what their kids were learning.",
            "Students who had homework routines in my class transitioned to middle school more successfully. Their teachers commented on their organizational skills."
        ],
        "experiences_B": [
            "I eliminated homework in my third-grade class and student stress levels dropped noticeably. Parents reported more peaceful evenings and better family relationships.",
            "I saw too many tears over homework that kids couldn't complete independently. It became about parent help rather than student learning.",
            "My students were exhausted after seven hours of school. When I stopped assigning homework, they came back more energetic and engaged the next day."
        ],
        "reasoning_A": [
            "The test score difference demonstrates that additional practice time strengthens understanding and recall of mathematical concepts.",
            "Parent involvement through homework created valuable communication channels between home and school about student progress.",
            "Early development of organizational skills gave students tools they needed for increased academic demands in higher grades."
        ],
        "reasoning_B": [
            "Eliminating homework stress allowed students to focus on learning rather than compliance, improving their overall relationship with education.",
            "Homework dependence on parent help creates inequity and doesn't assess student understanding accurately.",
            "Well-rested students have better attention and emotional regulation, making classroom time more effective than extended study hours."
        ],
        "category": "education"
    },
    {
        "id": "teacher_tenure",
        "probe": "Should public school teachers receive tenure protection after a few years of service?",
        "stance_A": "Yes, tenure protects teachers from political pressure and arbitrary dismissal, allowing them to advocate for students. I've seen excellent teachers fired for questioning bad policies or teaching controversial but important topics. Tenure lets me speak up at board meetings and try innovative methods without fear. Without it, teachers become afraid to challenge the status quo that often fails kids.",
        "stance_B": "No, tenure makes it nearly impossible to remove ineffective teachers who hurt student learning. I've worked alongside teachers who stopped trying once they got tenure, knowing they couldn't be fired. The lengthy process to dismiss tenured teachers costs districts hundreds of thousands while kids suffer in their classrooms. Merit should determine job security, not years of service.",
        "experiences_A": [
            "I challenged our district's plan to cut special education services at a board meeting. Without tenure, I would have been too afraid to speak out publicly.",
            "A non-tenured colleague was fired for teaching about evolution despite it being in the curriculum. The pressure from parents cost her job unfairly.",
            "I experimented with project-based learning that looked chaotic to administrators at first. Tenure gave me time to prove the method worked before being judged."
        ],
        "experiences_B": [
            "I watched a tenured teacher show movies daily for three years while students learned nothing. The principal tried to remove her but gave up after two years of documentation requirements.",
            "Our school had a teacher who verbally abused students but couldn't be fired because of tenure protections. Kids dreaded her class and parents complained constantly.",
            "The district spent $200,000 in legal fees trying to dismiss one tenured teacher. Meanwhile, we had to cut two teaching positions due to budget constraints."
        ],
        "reasoning_A": [
            "The ability to advocate publicly for students demonstrates how tenure protects educators from retaliation when they challenge harmful policies.",
            "The unjust firing shows how teachers without tenure can be dismissed for legitimate educational content when it becomes politically controversial.",
            "Academic freedom to try research-based methods requires protection from administrators who might not understand innovative approaches."
        ],
        "reasoning_B": [
            "The inability to remove an ineffective teacher shows how tenure can trap students with educators who have stopped meeting professional standards.",
            "Protection of abusive behavior demonstrates how tenure can shield teachers from appropriate consequences for harmful conduct toward students.",
            "The financial burden of dismissal procedures diverts resources from education while protecting teachers who may not deserve continued employment."
        ],
        "category": "education"
    },
    {
        "id": "school_choice_vouchers",
        "probe": "Should parents receive government vouchers to send their children to private schools?",
        "stance_A": "Yes, vouchers give parents the freedom to choose the best education for their children regardless of income. I've seen low-income families trapped in failing schools finally get access to quality private education through voucher programs. My daughter thrived in a small private school that addressed her learning differences in ways the public system couldn't. Competition forces all schools to improve.",
        "stance_B": "No, vouchers drain resources from public schools that serve most children and increase segregation. I've watched voucher programs primarily benefit middle-class families who could already afford private school tuition. Public money should strengthen public education for everyone, not subsidize private institutions that can discriminate in admissions.",
        "experiences_A": [
            "My neighbor used a voucher to move her son from a chaotic public school to a disciplined private academy. His grades went from D's to B's within one semester.",
            "I teach at a public school that improved dramatically after losing students to voucher schools. We finally had to address our discipline problems and outdated curriculum.",
            "A voucher program in our city allowed three low-income families I know to access private schools their children love. The individual attention transformed their confidence."
        ],
        "experiences_B": [
            "Our public school lost $500,000 to vouchers but still had to serve special needs students that private schools rejected. Class sizes increased and programs were cut.",
            "I researched voucher families in our district and found 80% already had one parent not working. Truly low-income families couldn't use them due to transportation and additional costs.",
            "A private school in our voucher program expelled students with behavior issues, sending them back to public schools mid-year. They kept the easy kids and voucher money."
        ],
        "reasoning_A": [
            "The dramatic improvement shows how school choice allows parents to find environments that better match their child's specific learning needs.",
            "Competitive pressure from voucher programs forced the public school to address longstanding problems it had previously ignored.",
            "Voucher access provided educational opportunities that these families could never have afforded, leveling the playing field based on merit rather than wealth."
        ],
        "reasoning_B": [
            "The funding loss created a double burden where public schools lost resources while retaining responsibility for harder-to-serve students.",
            "The demographic research reveals that vouchers primarily benefit families already positioned to access private education rather than truly expanding opportunity.",
            "The selective retention of students shows how private schools can manipulate voucher programs to maximize funding while minimizing challenging cases."
        ],
        "category": "education"
    },
    {
        "id": "year_round_school",
        "probe": "Should schools operate year-round with shorter, more frequent breaks instead of long summer vacations?",
        "stance_A": "Yes, year-round schooling prevents summer learning loss and better serves working families. I taught in a year-round school and students retained information much better without the three-month gap. Frequent two-week breaks throughout the year recharged everyone without the massive review time needed after summers. Parents appreciated consistent childcare instead of scrambling for summer coverage.",
        "stance_B": "No, the traditional school calendar works better for families and student development. I've seen year-round schools create scheduling nightmares for families with kids in different systems. Summer jobs and internships are crucial for teenagers, and many families depend on older siblings for childcare. The long break lets teachers recharge and pursue professional development.",
        "experiences_A": [
            "My year-round students started each term knowing what we'd learned before, while traditional calendar students needed six weeks of review after summer. We covered 20% more curriculum.",
            "I watched working parents stress about summer childcare costs and camps. Our year-round families had consistent schedules and shorter, cheaper break coverage needs.",
            "Students at our year-round school had fewer behavioral issues because they never got completely disconnected from school routines and expectations."
        ],
        "experiences_B": [
            "One family I knew had kids in year-round and traditional schools. They never took family vacations because someone was always in session or on break at different times.",
            "My high school students earned crucial income from summer jobs that helped pay for college. Year-round schedules would eliminate these opportunities.",
            "I used summers for intensive graduate courses and curriculum writing. The concentrated time off made me a much better teacher than scattered breaks would."
        ],
        "reasoning_A": [
            "Continuous learning without extended breaks allowed students to build knowledge cumulatively rather than repeatedly reviewing forgotten material.",
            "Year-round schedules aligned better with parents' work obligations, reducing family stress and childcare expenses throughout the year.",
            "Shorter breaks maintained school structure and relationships, preventing the behavioral regression that often occurs after long summer breaks."
        ],
        "reasoning_B": [
            "Incompatible school calendars within families created logistical problems that outweighed any educational benefits of year-round scheduling.",
            "Summer employment provided essential work experience and college funding that year-round schedules would eliminate for many students.",
            "Extended summer breaks allowed for intensive professional development opportunities that enhanced teaching quality more than frequent shorter breaks."
        ],
        "category": "education"
    },
    {
        "id": "single_sex_classes",
        "probe": "Should middle and high schools offer single-sex classes in core subjects?",
        "stance_A": "Yes, single-sex classes eliminate gender-based distractions and stereotypes that hurt learning. I taught both formats and girls participated much more actively in my all-female math classes, while boys engaged better in literature without worrying about looking uncool. Students can focus on learning rather than social dynamics. Same-sex environments let kids explore subjects without gender pressure.",
        "stance_B": "No, single-sex classes reinforce harmful gender stereotypes and don't prepare students for real-world collaboration. I've seen these programs assume girls need special help in math or boys can't handle cooperative learning. Coed classes teach students to work with everyone and challenge gender assumptions. Separation sends the message that boys and girls can't learn together effectively.",
        "experiences_A": [
            "In my all-girls physics class, participation jumped from 40% to 95%. Girls asked questions freely without fear of looking stupid in front of boys.",
            "I taught an all-male English class where boys openly discussed emotions in literature. They never would have shared those thoughts in mixed groups.",
            "Our single-sex math program eliminated the stereotype that girls aren't good at calculus. Female enrollment in advanced math doubled within three years."
        ],
        "experiences_B": [
            "I observed single-sex classes that reinforced stereotypes, with girls getting more collaborative activities and boys getting competitive approaches. This limited both groups' learning styles.",
            "Students from our single-sex program struggled in college where they had to work in mixed-gender groups. They lacked experience navigating those dynamics professionally.",
            "The all-boys classes I saw became more aggressive and rowdy without female classmates to moderate behavior. The classroom culture suffered significantly."
        ],
        "reasoning_A": [
            "Increased participation demonstrates that gender-based social pressure was previously inhibiting girls from engaging fully with challenging academic content.",
            "Male students' willingness to explore emotional topics shows how single-sex environments can free students from limiting gender expectations.",
            "Rising female enrollment in advanced courses proves that removing gender competition helped girls see themselves as capable in traditionally male-dominated subjects."
        ],
        "reasoning_B": [
            "Different instructional approaches based on gender reinforced limiting assumptions about how boys and girls learn rather than treating them as individuals.",
            "Students' college struggles show that artificial separation failed to prepare them for real-world mixed-gender academic and professional environments.",
            "Deteriorating classroom behavior suggests that gender diversity provides important social balance that improves the learning environment for everyone."
        ],
        "category": "education"
    },
    {
        "id": "school_start_times",
        "probe": "Should high schools start classes at 9 AM or later to align with teenage sleep patterns?",
        "stance_A": "Yes, later start times dramatically improve student health and academic performance. I've seen the research come to life - when our high school moved from 7:30 to 8:45 AM, tardiness dropped 40% and test scores increased. Teenagers' biological clocks make early mornings physically harmful. Students were more alert, less depressed, and had fewer car accidents after we changed.",
        "stance_B": "No, later start times create massive logistical problems that hurt families and student opportunities. I watched our district try later starts and it was a disaster - parents couldn't get to work, after-school jobs disappeared, and sports seasons got cut short. Real life starts early, and school should prepare students for that reality. The transportation costs alone weren't sustainable.",
        "experiences_A": [
            "When we shifted to 8:45 AM start, my first-period students went from half-asleep zombies to engaged learners. Participation in morning classes finally matched afternoon energy levels.",
            "Our school nurse reported 60% fewer students coming in sick or exhausted after we moved start times later. The health benefits were immediately obvious.",
            "Student parking lot accidents dropped dramatically with later starts. Tired teenage drivers were clearly a safety hazard we'd been ignoring."
        ],
        "experiences_B": [
            "Later start times meant my students couldn't work afternoon jobs that helped their families financially. Many had to choose between school activities and necessary income.",
            "Our bus system couldn't handle later high school starts without adding 20 more buses. The $2 million cost meant cutting music and art programs to balance the budget.",
            "Sports teams had to practice in the dark and couldn't host evening games because of time constraints. Our football season got shortened by three weeks."
        ],
        "reasoning_A": [
            "The dramatic improvement in morning class engagement proves that early start times were fighting against students' natural circadian rhythms.",
            "Reduced illness visits demonstrate that sleep deprivation was creating genuine health problems that later starts helped resolve.",
            "Fewer accidents show that early start times were putting teenagers at physical risk during their morning commutes to school."
        ],
        "reasoning_B": [
            "Lost employment opportunities harmed students who depend on after-school work, creating an unfair burden on families who need that income.",
            "Transportation costs show that later starts require significant resource reallocation that may not be financially sustainable for many districts.",
            "Shortened sports seasons demonstrate how later starts compress after-school activities that are important for student engagement and development."
        ],
        "category": "education"
    },
    {
        "id": "cellphones_classroom",
        "probe": "Should students be allowed to use cellphones during class for educational purposes?",
        "stance_A": "Yes, cellphones are powerful learning tools that engage students and prepare them for digital citizenship. I've used phones for research projects, polling, and connecting with experts around the world in real-time. Students are more motivated when they can use familiar technology for learning. Teaching responsible phone use is better than pretending smartphones don't exist in the modern world.",
        "stance_B": "No, cellphones in classrooms create constant distraction and undermine face-to-face learning. I've watched students text, play games, and browse social media while pretending to do research. Even when phones are supposed to be educational, they fragment attention and reduce deep thinking. Human interaction and focused concentration are disappearing because of device dependency.",
        "experiences_A": [
            "I had students use phones to interview elderly community members about local history. They created amazing documentary projects that combined technology with personal connections.",
            "We used classroom response apps on phones for real-time polls during discussions. Shy students who never spoke up suddenly participated actively through their devices.",
            "My students researched breaking news during current events lessons using phones. They learned to evaluate sources and fact-check in ways textbooks couldn't teach."
        ],
        "experiences_B": [
            "I tried allowing phones for research but caught students on Instagram and Snapchat instead. Even with clear guidelines, the temptation proved too strong for most.",
            "Student attention spans noticeably shortened when phones were present. They couldn't focus on one task for more than five minutes without checking their devices.",
            "Face-to-face discussions suffered when students could retreat to their phones. The quality of classroom conversation and debate declined significantly."
        ],
        "reasoning_A": [
            "The documentary project shows how phones can facilitate authentic learning experiences that connect students with their community in meaningful ways.",
            "Increased participation through polling apps demonstrates that technology can engage students who struggle with traditional classroom interaction methods.",
            "Real-time news research taught crucial media literacy skills that are essential for citizenship in the digital age."
        ],
        "reasoning_B": [
            "Student misuse despite clear rules proves that the addictive nature of social media makes phones incompatible with focused academic work.",
            "Shortened attention spans show that phone access trains students for constant stimulation rather than the sustained concentration learning requires.",
            "Declining discussion quality demonstrates that phones provide an escape from the challenging interpersonal skills students need to develop."
        ],
        "category": "education"
    },
    {
        "id": "arts_funding_priority",
        "probe": "Should schools prioritize arts programs equally with STEM subjects in funding and curriculum time?",
        "stance_A": "Yes, arts education is as essential as STEM for developing well-rounded, creative thinkers. I've seen students who struggled in traditional academics flourish in art, drama, and music classes, building confidence that carried over to other subjects. The creativity and problem-solving skills from arts programs are exactly what employers want. Cutting arts creates a narrow, test-focused education that fails to prepare students for real life.",
        "stance_B": "No, STEM skills are more critical for economic success and should receive priority in limited school budgets. I've watched arts programs consume resources that could have funded computer science or advanced math courses that actually prepare students for high-paying careers. While arts are nice, schools must focus on subjects that give students practical skills for the modern economy.",
        "experiences_A": [
            "My struggling math student became a confident leader after starring in the school play. That confidence transformed his academic performance across all subjects including mathematics.",
            "I taught students who landed internships at design firms and marketing companies because of skills learned in art class. Their creative abilities opened career doors STEM alone couldn't.",
            "Our school's jazz ensemble taught collaboration and improvisation skills that made those students better team members in science labs and engineering projects."
        ],
        "experiences_B": [
            "We spent $50,000 on a new theater sound system while our computer lab still had machines from 2010. Students needed coding skills more than better stage lighting.",
            "I watched talented art students graduate without basic technical literacy. They struggled to find jobs because employers demanded digital skills they'd never learned.",
            "Our state test scores dropped while we maintained full arts funding. Meanwhile, districts that prioritized math and science saw significant improvement in student outcomes."
        ],
        "reasoning_A": [
            "The student's transformation shows how arts success builds self-efficacy that transfers to academic subjects, creating a positive educational cycle.",
            "Real internship opportunities demonstrate that arts skills have direct economic value in creative industries that are growing rapidly.",
            "Cross-curricular benefits prove that arts education enhances STEM learning by developing collaboration and creative problem-solving abilities."
        ],
        "reasoning_B": [
            "The resource allocation disparity shows how arts spending can prevent investment in technology skills that are essential for modern employment.",
            "Graduate employment struggles illustrate that artistic talent without technical skills limits career opportunities in today's job market.",
            "Declining test scores suggest that equal arts funding may divert attention from core academic skills that students need for future success."
        ],
        "category": "education"
    },
    {
        "id": "cell_phones_classroom",
        "probe": "Should students be allowed to have cell phones in the classroom?",
        "stance_A": "Yes, students should have access to cell phones in class when used appropriately. I've used phones as research tools for instant fact-checking and accessing educational apps that enhance lessons. My students have used their cameras to document science experiments and collaborate on digital projects. Phones also provide crucial safety communication between students and parents during emergencies.",
        "stance_B": "No, cell phones should be banned from classrooms entirely. I constantly battle students texting, scrolling social media, and taking inappropriate photos instead of paying attention to instruction. Even when phones are supposedly put away, students are mentally distracted waiting for notifications. The classroom environment becomes chaotic when twenty students have potential distractions in their pockets.",
        "experiences_A": [
            "During our history lesson, students used their phones to quickly research primary sources and fact-check information, leading to rich classroom discussions.",
            "My biology students photographed their lab specimens and created digital portfolios that they shared with partner schools in other states.",
            "When our school had a lockdown, parents could text their children directly for reassurance instead of overwhelming the office phone lines."
        ],
        "experiences_B": [
            "I caught students filming TikTok videos during my literature discussion and taking photos of classmates without permission.",
            "Even with a 'phones away' policy, I saw students constantly glancing at their desks where phones were hidden, clearly distracted by notifications.",
            "My classroom management became impossible when students argued about phone use, with some claiming they were 'doing research' while clearly on Instagram."
        ],
        "reasoning_A": [
            "Phones enabled instant access to information that enriched academic discussions and supported inquiry-based learning.",
            "Digital documentation and sharing capabilities expanded learning beyond classroom walls and created authentic projects.",
            "Direct parent-student communication during emergencies provided safety and reduced administrative burden."
        ],
        "reasoning_B": [
            "Students misused phones for entertainment and violated peers' privacy instead of focusing on academic content.",
            "The anticipation of notifications created continuous mental distraction even when phones weren't actively being used.",
            "Phone-related conflicts and rule enforcement disrupted the learning environment and consumed instructional time."
        ],
        "category": "education"
    },
    {
        "id": "single_gender_classes",
        "probe": "Should schools offer single-gender classes or schools?",
        "stance_A": "Yes, single-gender education allows students to focus on learning without social distractions and gender stereotypes. My daughter thrived in an all-girls math class where she spoke up confidently and took leadership roles she never assumed in co-ed settings. I taught boys-only English classes where students engaged in emotional discussions about literature without worrying about impressing girls. Gender-separate environments eliminate many social pressures that inhibit academic risk-taking.",
        "stance_B": "No, single-gender education creates artificial barriers and reinforces harmful stereotypes about gender differences. I watched all-boys classes become more disruptive and competitive while all-girls classes became overly focused on perfectionism and conformity. My son needs to learn to work collaboratively with girls since that's the real world he'll enter. Separating genders sends the message that boys and girls can't learn effectively together.",
        "experiences_A": [
            "My shy daughter became a confident leader in her all-girls science class, asking questions and conducting experiments she never would have attempted with boys present.",
            "I taught an all-boys poetry unit where students shared deeply personal writing and emotions they typically hide in mixed-gender classes.",
            "Girls in my single-gender math class pursued advanced calculus at twice the rate of girls in co-educational sections."
        ],
        "experiences_B": [
            "The all-boys class I observed was chaotic and aggressive, with students trying to out-masculine each other instead of focusing on academics.",
            "My daughter's all-girls class became obsessed with perfectionism and social comparison, creating more anxiety than learning.",
            "Students from single-gender middle school struggled socially when they reached co-educational high school, lacking skills for mixed-gender collaboration."
        ],
        "reasoning_A": [
            "Removal of opposite-gender social pressure allowed the student to take academic and leadership risks.",
            "Boys felt safe expressing vulnerability and emotions without fear of gender-based judgment.",
            "Elimination of gender stereotypes in mathematics led to increased female participation in advanced coursework."
        ],
        "reasoning_B": [
            "Gender segregation amplified negative masculine behaviors and created a competitive rather than collaborative environment.",
            "Single-gender settings intensified social pressures within the group rather than eliminating them.",
            "Lack of mixed-gender interaction during formative years impaired social development needed for adult success."
        ],
        "category": "education"
    },
    {
        "id": "arts_education_cuts",
        "probe": "Should schools maintain arts programs even when facing budget constraints?",
        "stance_A": "Yes, arts education is essential and should be protected even during budget cuts. I watched my struggling son find confidence and academic improvement through theater class - his grades in other subjects improved when he felt successful in drama. Arts programs serve students who don't excel in traditional academics and provide crucial creative outlets. The skills learned in music and art - discipline, creativity, collaboration - transfer to all other areas of learning.",
        "stance_B": "No, when budgets are tight, schools must prioritize core academic subjects that directly impact standardized test scores and college readiness. I've seen schools maintain expensive music programs while cutting math tutoring and reading specialists that struggling students desperately need. Arts are enriching but not essential when students can't read at grade level. Limited resources should go to programs that address fundamental academic deficiencies first.",
        "experiences_A": [
            "My son was failing academically until he joined the school band. The discipline and success he found in music motivated him to improve his grades in all subjects.",
            "I taught students who only came to school for art class - without that program, they would have dropped out entirely.",
            "Our school's theater program taught students public speaking, memorization, and teamwork skills that improved their performance in English and history classes."
        ],
        "experiences_B": [
            "Our district kept the expensive orchestra program but eliminated reading specialists, leaving 30% of third-graders unable to read at grade level.",
            "I saw the art teacher's salary fund three math tutoring positions that helped 150 struggling students pass algebra.",
            "When forced to choose, parents overwhelmingly requested academic support over arts programs at our budget meeting."
        ],
        "reasoning_A": [
            "Arts engagement improved overall academic motivation and performance through building student confidence and engagement.",
            "Creative programs provided the only school connection for at-risk students, preventing dropouts.",
            "Arts instruction developed transferable skills that enhanced performance in traditional academic subjects."
        ],
        "reasoning_B": [
            "Funding for arts prevented investment in basic literacy programs needed by a significant portion of students.",
            "Arts program costs could fund multiple academic intervention programs serving many more students.",
            "Community priorities favored fundamental academic skills over enrichment when resources were limited."
        ],
        "category": "education"
    },
    {
        "id": "parent_teacher_conferences",
        "probe": "Should parent-teacher conferences be mandatory for all parents?",
        "stance_A": "Yes, mandatory parent-teacher conferences ensure all students have advocates and parents stay informed about their education. I've seen dramatic improvement in students whose previously uninvolved parents were required to attend conferences and learned about academic struggles. When conferences are optional, the parents who need to come most often don't show up. Mandatory meetings create partnership between home and school that benefits every child's learning.",
        "stance_B": "No, forcing parents to attend conferences creates resentment and doesn't improve student outcomes when parents are there unwillingly. I held mandatory conferences with hostile parents who felt attacked and defensive rather than collaborative. Some parents work multiple jobs or have transportation challenges that make required meetings impossible. Voluntary conferences with engaged parents are more productive than mandatory ones with resistant families.",
        "experiences_A": [
            "A student was failing until I required his parent to attend a conference. The mother discovered he needed glasses and wasn't doing homework - his grades improved immediately.",
            "Mandatory conferences helped me identify three cases of learning disabilities that parents hadn't recognized, leading to proper support services.",
            "When conferences were optional, only 40% of parents attended. Making them required meant struggling students finally got the home support they needed."
        ],
        "experiences_B": [
            "I spent 30 minutes with an angry father who resented being forced to take time off work. He argued with every suggestion and left more hostile than when he arrived.",
            "A single mother missed the mandatory conference due to her night shift job and received threatening letters from the school about truancy court.",
            "My most productive conversations happened with parents who chose to meet with me multiple times, not those required to attend once."
        ],
        "reasoning_A": [
            "Required attendance ensured parents learned about academic and health issues affecting their child's performance.",
            "Mandatory conferences identified learning disabilities that might have gone unaddressed with voluntary meetings.",
            "Higher attendance rates meant more students received home support that improved academic outcomes."
        ],
        "reasoning_B": [
            "Forced attendance created adversarial relationships that prevented productive collaboration between parents and teachers.",
            "Rigid requirements penalized parents facing economic or logistical challenges beyond their control.",
            "Voluntary engagement produced more meaningful relationships and ongoing support than mandatory single meetings."
        ],
        "category": "education"
    },
    {
        "id": "renewable_subsidies",
        "probe": "Should governments provide subsidies for residential solar panel installation?",
        "stance_A": "Yes, solar subsidies accelerate clean energy adoption and benefit everyone. I installed panels with rebate help and now generate more power than I use, feeding clean electricity back to the grid. These programs create jobs, reduce grid strain during peak hours, and help achieve climate goals faster than market forces alone.",
        "stance_B": "No, solar subsidies are regressive welfare for the wealthy. I rent my apartment and can't access these programs, yet my taxes fund rebates for homeowners who could afford panels anyway. The subsidies distort markets, and I've seen installers inflate prices knowing government money is available.",
        "experiences_A": [
            "I got a 30% rebate on my solar installation and now sell excess power back to the utility, reducing my neighbors' peak demand.",
            "My brother works for a solar company that hired 50 people since residential subsidies expanded in our state.",
            "I watched our community reach 40% renewable energy faster than projected thanks to widespread residential adoption."
        ],
        "experiences_B": [
            "I compared solar quotes before and after subsidies launched - installers raised prices by almost exactly the rebate amount.",
            "My property taxes fund programs I can't use as a renter, while my wealthy homeowner friends get thousands in rebates.",
            "I've seen multiple solar companies go bankrupt when subsidy programs ended, leaving customers with worthless warranties."
        ],
        "reasoning_A": [
            "Selling excess power back demonstrates how residential solar creates distributed generation benefits for the whole grid.",
            "Job creation shows subsidies stimulate economic activity beyond just the environmental benefits.",
            "Faster renewable adoption proves subsidies accelerate climate goals that benefit everyone."
        ],
        "reasoning_B": [
            "Price inflation suggests subsidies create market inefficiencies that waste taxpayer money.",
            "The renter-homeowner disparity shows subsidies transfer wealth from renters to property owners.",
            "Company bankruptcies reveal how subsidy-dependent industries lack sustainable business models."
        ],
        "category": "environment"
    },
    {
        "id": "urban_car_restrictions",
        "probe": "Should cities restrict private car access in downtown areas?",
        "stance_A": "Yes, car restrictions transform cities for the better. I've worked in downtown areas with limited car access and the air quality, noise levels, and walkability are dramatically better. Public transit improves when cities prioritize it, and local businesses thrive when people can safely walk around instead of driving through.",
        "stance_B": "No, car restrictions hurt accessibility and economic activity. I've seen elderly and disabled people unable to access downtown services when driving was restricted. Small businesses lose customers who can't easily drive and park, and public transit often isn't reliable enough to replace cars for many trips.",
        "experiences_A": [
            "I moved my office to a car-free downtown district and productivity increased - employees bike to work and take walking meetings instead of sitting in traffic.",
            "My neighborhood restaurant's outdoor seating expanded into former parking spots, doubling their capacity after car restrictions.",
            "I measured air quality in our pedestrian zone - particulate matter dropped 40% after private cars were banned."
        ],
        "experiences_B": [
            "My 80-year-old mother stopped visiting downtown shops after parking was eliminated - the bus stop is too far from her doctor's office.",
            "I watched foot traffic at my friend's downtown store drop 30% when they restricted car access, forcing him to relocate.",
            "I regularly take rideshares downtown because our bus system is unreliable, but now they're banned from the core area too."
        ],
        "reasoning_A": [
            "Increased employee productivity shows car restrictions create healthier, more pleasant work environments.",
            "Restaurant expansion demonstrates how reclaimed street space creates economic opportunities.",
            "Measurable air quality improvement proves car restrictions deliver concrete health benefits."
        ],
        "reasoning_B": [
            "Elderly people losing access shows restrictions can exclude those who need cars for mobility.",
            "Store closures prove restrictions can harm small businesses that depend on car-driving customers.",
            "Rideshare complications highlight how restrictions can create transportation gaps when transit is inadequate."
        ],
        "category": "environment"
    },
    {
        "id": "factory_farming_regulation",
        "probe": "Should governments ban or heavily regulate factory farming operations?",
        "stance_A": "Yes, factory farming causes immense environmental and ethical damage that requires regulation. I've lived near industrial livestock operations and witnessed the water contamination, air pollution, and animal suffering firsthand. These facilities concentrate waste, overuse antibiotics, and contribute significantly to greenhouse gas emissions.",
        "stance_B": "No, heavy regulation would devastate food affordability and rural economies. I grew up on a family farm and saw how modern agricultural methods feed more people efficiently. Strict regulations would force production overseas with worse standards, and meat prices would skyrocket, hurting working families most.",
        "experiences_A": [
            "I lived downwind from a large pig farm and couldn't open windows for months due to the overwhelming ammonia smell and flies.",
            "My well water tested positive for nitrates after a chicken operation opened nearby, forcing me to buy bottled water.",
            "I toured a factory farm and saw thousands of chickens crammed in windowless sheds, many with injuries and infections."
        ],
        "experiences_B": [
            "My family's farm feeds 10 times more people per acre than it did in my grandfather's day using modern intensive methods.",
            "I watched small ranchers go out of business when environmental regulations made their operations uneconomical.",
            "My grocery budget increased 40% when I tried buying only pasture-raised meat - factory farming keeps protein affordable."
        ],
        "reasoning_A": [
            "Persistent odor and pest problems show factory farms create serious quality of life issues for surrounding communities.",
            "Water contamination demonstrates how concentrated animal operations pose public health risks.",
            "Direct observation of animal conditions reveals the ethical problems inherent in industrial farming."
        ],
        "reasoning_B": [
            "Increased food production efficiency shows modern methods are necessary to feed growing populations affordably.",
            "Small farm closures suggest heavy regulation could consolidate agriculture in fewer, potentially worse operations.",
            "Personal budget impacts prove that alternatives remain economically inaccessible for most consumers."
        ],
        "category": "environment"
    },
    {
        "id": "nuclear_waste_storage",
        "probe": "Should communities be required to accept nuclear waste storage facilities?",
        "stance_A": "Yes, we need centralized nuclear waste storage and communities must participate. I've studied the safety records of existing facilities and they're remarkably safe with proper engineering. Nuclear waste is already distributed across dozens of temporary sites - consolidating it in a purpose-built facility is far safer than the current situation.",
        "stance_B": "No, no community should be forced to store nuclear waste. I live near a proposed storage site and we don't want the risk of accidents or transportation mishaps. These facilities become permanent regardless of promises, and property values plummet just from the proposal. Let the utilities that profited deal with their own waste.",
        "experiences_A": [
            "I worked at a temporary nuclear storage facility for five years - we never had a single safety incident despite handling highly radioactive materials daily.",
            "I researched Finland's deep geological repository and their engineering solutions for 10,000-year containment are incredibly sophisticated.",
            "My town hosts a low-level nuclear waste facility and it's been our safest industrial operation for 30 years, with good-paying jobs."
        ],
        "experiences_B": [
            "Home values in my neighborhood dropped 25% just from rumors about a nuclear waste facility, before any decision was made.",
            "I attended community meetings where government officials couldn't answer basic questions about accident response plans.",
            "My cousin lives near Yucca Mountain and they're still fighting a nuclear dump that was supposed to be 'temporary' 40 years ago."
        ],
        "reasoning_A": [
            "Zero safety incidents over five years demonstrates that nuclear waste can be handled safely with proper procedures.",
            "Finland's advanced repository shows that permanent geological storage solutions are technically feasible.",
            "The 30-year safety record proves nuclear facilities can operate safely while providing economic benefits."
        ],
        "reasoning_B": [
            "Immediate property value drops show nuclear waste storage imposes real economic costs on unwilling communities.",
            "Officials' inability to answer safety questions suggests inadequate planning and transparency.",
            "Yucca Mountain's decades-long controversy demonstrates how 'temporary' nuclear storage becomes permanent."
        ],
        "category": "environment"
    },
    {
        "id": "water_privatization",
        "probe": "Should cities privatize their water utilities to private companies?",
        "stance_A": "Yes, private water management brings efficiency and innovation that cash-strapped cities need. I've seen private utilities upgrade aging infrastructure faster and provide better customer service than bureaucratic public systems. Competition and profit motives drive performance improvements that benefit everyone through cleaner, more reliable water.",
        "stance_B": "No, water is a human right that shouldn't be profit-driven. I lived through a water privatization and watched rates skyrocket while service quality declined. Private companies cut corners on maintenance and testing to maximize profits, and low-income families suffer most when water becomes a luxury good.",
        "experiences_A": [
            "After our water system was privatized, I got 24/7 customer service and same-day repair responses instead of waiting weeks for city crews.",
            "I witnessed a private utility replace 50 miles of century-old pipes that the city had ignored for decades due to budget constraints.",
            "My water quality improved measurably after privatization - the company invested in modern filtration systems the municipality couldn't afford."
        ],
        "experiences_B": [
            "My water bill tripled within five years of privatization, forcing me to choose between water and other necessities.",
            "I discovered our private water company was falsifying water quality tests to avoid expensive treatments.",
            "When pipes burst in my neighborhood, the private company took three days to respond because it wasn't in a wealthy area."
        ],
        "reasoning_A": [
            "Faster customer service shows private companies have stronger incentives to maintain customer satisfaction.",
            "Major infrastructure investments demonstrate how private capital can address public sector budget limitations.",
            "Water quality improvements prove private operators can deliver better technical performance."
        ],
        "reasoning_B": [
            "Tripled bills show how profit maximization can make essential services unaffordable for residents.",
            "Falsified testing reveals how private companies may compromise safety to reduce costs.",
            "Delayed emergency response in poor areas demonstrates how privatization can create service inequities."
        ],
        "category": "environment"
    },
    {
        "id": "organic_food_mandates",
        "probe": "Should schools be required to serve only organic food in their cafeterias?",
        "stance_A": "Yes, schools should serve organic food to protect children's health and development. I've seen kids' behavior and focus improve dramatically when schools eliminated pesticide-laden foods. Children are more vulnerable to chemical exposure, and school meals reach the kids who need healthy food most. The long-term health benefits justify the extra cost.",
        "stance_B": "No, organic mandates would make school meals unaffordable and reduce nutrition access. I've managed school food budgets and organic requirements would either bankrupt programs or force us to serve less food to fewer kids. Many organic claims aren't scientifically proven, and conventional farming feeds more children affordably.",
        "experiences_A": [
            "I teach at a school that switched to organic meals and saw significant improvements in student attention and classroom behavior within months.",
            "My daughter's school went organic and allergy incidents dropped by half - fewer kids reacting to pesticides and additives.",
            "I volunteer in lunch programs and noticed kids actually eat more organic vegetables than the processed conventional alternatives."
        ],
        "experiences_B": [
            "Our district priced out organic menus and would have to cut the free lunch program by 40% to afford it.",
            "I compared nutritional labels and many organic processed foods have identical ingredients to conventional versions at double the price.",
            "My rural school district struggles to source fresh organic produce reliably - we'd have to serve less variety and nutrition."
        ],
        "reasoning_A": [
            "Improved student behavior suggests organic foods reduce exposure to chemicals that affect developing brains.",
            "Fewer allergic reactions indicates organic foods eliminate problematic pesticides and additives.",
            "Better vegetable consumption shows organic options can improve children's eating habits and nutrition."
        ],
        "reasoning_B": [
            "Budget constraints prove organic mandates could reduce food access for the most vulnerable students.",
            "Identical processed food ingredients show organic labeling doesn't always guarantee better nutrition.",
            "Supply chain difficulties demonstrate organic mandates may reduce meal variety and overall nutrition."
        ],
        "category": "environment"
    },
    {
        "id": "green_building_codes",
        "probe": "Should cities mandate green building standards for all new construction?",
        "stance_A": "Yes, green building codes are essential for sustainable development. I've lived in LEED-certified buildings and the energy savings, air quality, and comfort are dramatically better than conventional construction. Mandates drive market adoption faster than voluntary programs, and climate change requires immediate action on building efficiency.",
        "stance_B": "No, green building mandates increase housing costs when affordability is already a crisis. I've seen construction projects cancelled because green requirements made them financially unfeasible. Many green standards are expensive feel-good measures with minimal environmental impact, and we need more housing supply, not perfect buildings.",
        "experiences_A": [
            "My green-certified office building uses 60% less energy than our previous conventional space, saving thousands in utility costs annually.",
            "I developed a LEED project and the integrated design process actually reduced overall construction costs through efficiency gains.",
            "My apartment in a green building has measurably better indoor air quality and I haven't been sick once since moving in."
        ],
        "experiences_B": [
            "I had to cancel an affordable housing project because green requirements added $15,000 per unit we couldn't finance.",
            "My contractor friend says green certification paperwork adds months to projects while creating minimal actual environmental benefit.",
            "I compared energy bills in green versus conventional apartments and found negligible differences despite 30% higher rent."
        ],
        "reasoning_A": [
            "Dramatic energy savings demonstrate green buildings deliver measurable environmental and economic benefits.",
            "Reduced construction costs through integrated design show green standards can improve efficiency beyond just environmental metrics.",
            "Better health outcomes prove green buildings create tangible quality of life improvements for occupants."
        ],
        "reasoning_B": [
            "Cancelled affordable housing shows green mandates can worsen housing shortages by making projects unviable.",
            "Excessive paperwork suggests green codes create bureaucratic burdens without proportional environmental gains.",
            "Similar energy performance despite higher costs indicates green premiums may not deliver promised benefits."
        ],
        "category": "environment"
    },
    {
        "id": "electric_vehicle_mandates",
        "probe": "Should governments ban the sale of new gasoline-powered vehicles by 2035?",
        "stance_A": "Yes, we need firm deadlines to accelerate the transition to electric vehicles. I've driven EVs for three years and they're superior to gas cars in performance, maintenance, and operating costs. Automakers only invest seriously in new technology when forced by regulation, and climate goals require rapid transportation decarbonization.",
        "stance_B": "No, EV mandates ignore real infrastructure and affordability barriers. I live in rural areas where charging stations are scarce and unreliable, making EVs impractical for daily life. Used EV prices remain high, and many people can't afford new cars or home charging equipment. Let market demand drive adoption naturally.",
        "experiences_A": [
            "I switched to an EV and my transportation costs dropped by $3,000 annually between fuel and maintenance savings.",
            "My Tesla has better acceleration and handling than any gas car I've owned, plus I charge it at home overnight.",
            "I watched automakers announce massive EV investments only after California and other states set gas car phase-out dates."
        ],
        "experiences_B": [
            "I drove 200 miles to visit family and found three broken charging stations before locating one that worked, adding two hours to my trip.",
            "My apartment complex won't install EV chargers and the nearest public station is 15 minutes away, making ownership impractical.",
            "I priced used EVs and they're still $10,000 more than equivalent gas cars, plus I'd need expensive home electrical upgrades."
        ],
        "reasoning_A": [
            "Significant cost savings show EVs offer compelling economic advantages once adoption barriers are overcome.",
            "Superior vehicle performance demonstrates EVs are technically ready to replace gas cars for most users.",
            "Automaker investment timing proves regulatory pressure is necessary to drive industry transformation."
        ],
        "reasoning_B": [
            "Charging infrastructure failures show the support network isn't ready for mass EV adoption.",
            "Lack of apartment charging access reveals how EVs remain impractical for many living situations.",
            "Price premiums and upgrade costs demonstrate EVs aren't financially accessible for most consumers."
        ],
        "category": "environment"
    },
    {
        "id": "plastic_bag_bans",
        "probe": "Should cities ban single-use plastic bags in retail stores?",
        "stance_A": "Yes, plastic bag bans are a crucial step toward reducing waste. Since my city banned plastic bags, I see dramatically less litter in parks and waterways. The adjustment period was brief - everyone adapted quickly to reusable bags. These bans force a simple behavior change that prevents millions of bags from ending up in landfills and oceans.",
        "stance_B": "No, plastic bag bans create more problems than they solve. I've watched people struggle with heavy groceries and resort to buying thicker plastic bags instead. Many customers forget reusable bags and end up purchasing new ones repeatedly. The bans disproportionately burden elderly and low-income shoppers who relied on free bags for household needs.",
        "experiences_A": [
            "After our plastic bag ban, the amount of litter in my neighborhood park dropped noticeably. Cleanup volunteers collect 70% fewer plastic bags.",
            "I adapted to reusable bags within a month. Now I always keep bags in my car and it's second nature.",
            "Local beaches have way less plastic debris since the ban. Marine wildlife rescue reports fewer animals with plastic ingestion."
        ],
        "experiences_B": [
            "I see elderly customers at the grocery store struggling to carry items without handles. Many buy the thicker 'reusable' plastic bags every trip.",
            "My low-income neighbors used free plastic bags as trash liners. Now they have to buy garbage bags, adding to their expenses.",
            "Paper bag production increased 400% in our city after the ban. The environmental impact just shifted to different materials."
        ],
        "reasoning_A": [
            "Reduced litter demonstrates the ban directly addresses the environmental problem plastic bags create in public spaces.",
            "Quick adaptation shows consumers can easily change habits when given the right incentives.",
            "Fewer wildlife injuries prove the ban reduces harmful plastic pollution in marine ecosystems."
        ],
        "reasoning_B": [
            "Customers buying thicker bags shows the ban can increase rather than decrease plastic consumption.",
            "Added expenses for trash bags disproportionately burden people who relied on free bags for essential household functions.",
            "Increased paper production suggests the environmental benefits may be offset by other forms of resource consumption and pollution."
        ],
        "category": "environment"
    },
    {
        "id": "urban_sprawl_limits",
        "probe": "Should cities restrict suburban development to prevent urban sprawl?",
        "stance_A": "Yes, we must limit suburban sprawl to protect farmland and reduce car dependence. I live in a city with strong growth boundaries and our downtown thrives while preserving nearby agricultural land. Dense neighborhoods create walkable communities with better public transit. Unrestricted sprawl destroys natural habitats and forces everyone to drive everywhere for basic needs.",
        "stance_B": "No, restricting suburban development makes housing unaffordable and limits personal choice. I've seen how growth restrictions drive up home prices and force working families further from job centers. People should have the freedom to choose where they live. Many families prefer suburban neighborhoods with yards and good schools over cramped urban apartments.",
        "experiences_A": [
            "Portland's urban growth boundary preserved the Columbia River Gorge and Hood River valley farms. I can reach pristine nature in 30 minutes from downtown.",
            "My dense neighborhood has three coffee shops, two grocery stores, and a pharmacy within walking distance. I rarely need to drive.",
            "Vancouver's density limits created vibrant neighborhoods. Property values rose but so did quality of life and transit options."
        ],
        "experiences_B": [
            "Housing prices in San Francisco skyrocketed due to development restrictions. My teacher friends had to move two hours away to afford homes.",
            "I grew up in suburbs with safe streets and yards for kids to play. Dense urban living isn't suitable for every family's needs.",
            "Seattle's growth management pushed development to distant exurbs. People now commute 90 minutes each way, creating more sprawl and emissions."
        ],
        "reasoning_A": [
            "Preserved farmland and natural areas show growth boundaries successfully protect valuable ecosystems and agricultural resources from development.",
            "Walkable neighborhoods demonstrate how density limits can create more sustainable transportation patterns and reduce car dependence.",
            "Improved transit and amenities prove density can enhance rather than diminish urban quality of life."
        ],
        "reasoning_B": [
            "Rising housing costs show development restrictions can make cities unaffordable for middle-class families and essential workers.",
            "Family preferences for suburban living demonstrate that density limits can conflict with legitimate lifestyle choices and needs.",
            "Longer commutes from distant areas prove overly restrictive policies can backfire by pushing development to even more car-dependent locations."
        ],
        "category": "environment"
    },
    {
        "id": "industrial_farming_regulation",
        "probe": "Should governments heavily regulate large-scale industrial farming operations?",
        "stance_A": "Yes, industrial agriculture needs strict oversight to protect public health and the environment. I live near factory farms and have witnessed groundwater contamination and air quality problems firsthand. These operations externalize massive environmental costs while consolidating agricultural power. Stronger regulations would level the playing field for smaller farms practicing sustainable methods.",
        "stance_B": "No, over-regulating agriculture threatens food security and rural livelihoods. I work in agricultural production and know that large operations achieve efficiency and affordability that feed millions. Heavy regulations would drive up food costs and push production to countries with weaker standards. Modern farming technology has greatly improved environmental performance when market incentives align properly.",
        "experiences_A": [
            "The creek near my home turned green with algae after a large dairy operation expanded upstream. Fish kills happened twice last summer.",
            "I documented air quality issues around a massive hog operation. Neighbors developed respiratory problems and property values dropped significantly.",
            "Small organic farms in my area struggle to compete with subsidized industrial operations that don't pay for environmental cleanup."
        ],
        "experiences_B": [
            "Modern poultry operations use 75% less land and water per pound of meat than they did 30 years ago. Technology drives efficiency improvements.",
            "When California's Proposition 12 restricted egg production, prices jumped 40% and supply came from out-of-state operations with potentially worse conditions.",
            "The grain elevator I manage serves 150 family farms. Regulatory compliance costs already consume 20% of their margins."
        ],
        "reasoning_A": [
            "Water pollution demonstrates how industrial operations can impose significant environmental costs on surrounding communities.",
            "Health impacts and property value declines show industrial farming creates negative externalities that aren't reflected in market prices.",
            "Competitive disadvantages for sustainable farms prove current regulations fail to account for environmental benefits of alternative practices."
        ],
        "reasoning_B": [
            "Efficiency improvements show modern industrial agriculture has reduced its environmental footprint per unit of production.",
            "Price increases and supply shifts demonstrate how regulations can make food less affordable while potentially relocating rather than solving problems.",
            "High compliance costs for family farms show excessive regulation can harm smaller operations that regulations are meant to protect."
        ],
        "category": "environment"
    },
    {
        "id": "renewable_energy_mandates",
        "probe": "Should states require utilities to generate a minimum percentage of electricity from renewable sources?",
        "stance_A": "Yes, renewable portfolio standards are essential for clean energy transition. My state's 30% renewable mandate drove massive wind development that now provides cheap, clean electricity. Utilities won't make the transition voluntarily due to sunk costs in fossil fuel infrastructure. Mandates create certainty that attracts investment and accelerates cost reductions through scale.",
        "stance_B": "No, renewable mandates increase electricity costs and threaten grid reliability. I've seen firsthand how rushed renewable development led to blackouts when the wind didn't blow. Market forces are already driving renewable adoption as costs fall. Mandates force premature retirement of reliable power plants and require expensive backup systems that customers pay for.",
        "experiences_A": [
            "Texas's renewable mandate sparked a wind boom. We now have the cheapest electricity in decades and lead the nation in clean energy jobs.",
            "California's renewable standard drove solar costs down 85%. My utility bills are lower now than before the mandate took effect.",
            "Portfolio standards gave developers certainty to invest. Three wind farms were built in my county, bringing $50 million in property tax revenue."
        ],
        "experiences_B": [
            "During the Texas freeze, wind turbines stopped working and we lost power for 3 days. Over-reliance on renewables created vulnerability.",
            "Germany's renewable push led to the highest electricity prices in Europe. Industrial companies started moving production elsewhere.",
            "Our utility had to build expensive natural gas plants to back up solar farms. Customers pay twice - for the renewables and the backup."
        ],
        "reasoning_A": [
            "Wind development success shows mandates can create thriving clean energy industries that provide economic benefits beyond environmental ones.",
            "Falling costs demonstrate how policy-driven scale can accelerate technology improvement and make renewables more affordable.",
            "Investment certainty proves mandates solve the coordination problem that prevents optimal renewable deployment in competitive markets."
        ],
        "reasoning_B": [
            "Grid failures during extreme weather demonstrate renewable intermittency can create reliability risks that threaten essential services.",
            "High electricity prices show renewable mandates can impose significant economic costs on consumers and businesses.",
            "Backup generation requirements prove renewable mandates can increase rather than decrease total system costs."
        ],
        "category": "environment"
    },
    {
        "id": "electric_vehicle_incentives",
        "probe": "Should governments provide tax incentives for electric vehicle purchases?",
        "stance_A": "Yes, EV incentives are crucial for accelerating the transition to clean transportation. The $7,500 federal tax credit made my Tesla affordable and I've saved thousands on gas. These incentives help overcome the higher upfront costs while the technology scales up. Transportation is the largest source of emissions - we need policy support to break oil dependence.",
        "stance_B": "No, EV subsidies are corporate welfare that benefit wealthy buyers at taxpayer expense. Most people claiming the tax credit earn over $100,000 and would buy EVs anyway. I'm subsidizing luxury cars I can't afford while driving a used Honda. Market forces will drive EV adoption naturally as batteries get cheaper without government picking winners.",
        "experiences_A": [
            "The $7,500 federal credit made my Model 3 purchase possible. I've saved $3,000/year on gas and maintenance over three years of ownership.",
            "Norway's generous EV incentives led to 80% electric car sales. Their cities have dramatically cleaner air and less traffic noise.",
            "Local utility rebates helped my neighbor afford a used Leaf. Even middle-class families can access EVs with the right incentives."
        ],
        "experiences_B": [
            "I calculated that 78% of EV tax credits in my zip code went to households earning over $150,000. Working-class people subsidize luxury cars.",
            "My property taxes went up to fund EV charging stations I'll never use. Public money should go to transit, not private vehicle subsidies.",
            "EV prices are already falling fast without subsidies. Tesla has cut prices three times this year as competition increases."
        ],
        "reasoning_A": [
            "Personal savings on fuel and maintenance show incentives can make EVs economically attractive while supporting early adoption.",
            "Norway's transformation demonstrates how strong policy incentives can rapidly shift entire transportation systems toward electrification.",
            "Used EV accessibility proves incentives can expand beyond luxury buyers to help middle-income families participate in the transition."
        ],
        "reasoning_B": [
            "Income distribution of credit recipients shows EV incentives function as regressive transfers from all taxpayers to higher-income buyers.",
            "Infrastructure costs demonstrate how EV support extends beyond purchase incentives to ongoing public investments that may not be equitable.",
            "Falling prices without subsidies suggest market forces are sufficient to drive adoption without government intervention."
        ],
        "category": "environment"
    },
    {
        "id": "forest_logging_restrictions",
        "probe": "Should governments restrict logging in old-growth forests to protect biodiversity?",
        "stance_A": "Yes, we must protect remaining old-growth forests for biodiversity and climate stability. I've hiked through 800-year-old stands that support species found nowhere else. These forests store massive amounts of carbon and provide irreplaceable ecosystem services. Once cut, it takes centuries to restore old-growth characteristics. The economic value of intact forests exceeds short-term timber profits.",
        "stance_B": "No, logging restrictions destroy rural communities and ignore sustainable forestry practices. I work in the timber industry and have seen how preservation policies eliminated thousands of jobs in small towns. Modern selective harvesting can maintain forest health while supporting local economies. Many forests actually benefit from active management to prevent catastrophic wildfires and disease outbreaks.",
        "experiences_A": [
            "I documented spotted owls in Pacific Northwest old-growth that disappeared after nearby clear-cuts. These species need intact forest canopies to survive.",
            "Carbon measurements show old-growth forests store 3-5 times more carbon per acre than managed forests. They're crucial climate buffers.",
            "Tourism in my area generates $200 million annually from people visiting ancient forests. The economic value exceeds timber harvests."
        ],
        "experiences_B": [
            "My hometown lost 4,000 jobs when the national forest closed to logging. The school system and hospital nearly collapsed from the tax base decline.",
            "Unthinned forests in my area suffered catastrophic fires that killed more wildlife than decades of selective logging ever did.",
            "I manage 500 acres using sustainable practices. Selective harvests every 20 years maintain forest health while generating income for conservation."
        ],
        "reasoning_A": [
            "Species loss demonstrates old-growth forests provide unique habitat that cannot be replicated in managed forests or plantations.",
            "Carbon storage data shows old-growth protection is essential for climate change mitigation and forest carbon sequestration goals.",
            "Tourism revenue proves intact forests can generate sustainable economic value without destructive extraction."
        ],
        "reasoning_B": [
            "Job losses show logging restrictions can devastate rural communities that depend on forest industries for economic stability.",
            "Wildfire damage demonstrates that some forest management interventions may be necessary to maintain ecosystem health and wildlife populations.",
            "Sustainable harvesting success proves that logging and conservation goals can be compatible with proper management practices."
        ],
        "category": "environment"
    },
    {
        "id": "water_usage_restrictions",
        "probe": "Should cities impose strict water usage restrictions during drought periods?",
        "stance_A": "Yes, mandatory water restrictions are essential during droughts to ensure adequate supply. I lived through California's historic drought and saw how conservation measures prevented complete reservoir depletion. Voluntary efforts don't work - usage barely declined until fines were imposed. Water is a shared resource that requires collective action when supplies are threatened.",
        "stance_B": "No, water restrictions punish responsible users while ignoring the real waste. I maintain a small garden and face fines while agriculture uses 80% of our water. Pricing mechanisms work better than rationing - let people pay for what they use. Many restrictions are arbitrary and don't address the biggest consumption sources or long-term supply solutions.",
        "experiences_A": [
            "During California's drought, mandatory restrictions cut urban water use by 25%. Reservoirs stabilized and we avoided complete system failure.",
            "My neighborhood's lawn watering limits prevented wells from running dry. Some suburbs without restrictions lost water pressure entirely.",
            "Cape Town's strict rationing helped them avoid 'Day Zero' when taps would have run completely dry for 4 million people."
        ],
        "experiences_B": [
            "I reduced my water use 40% voluntarily but still got cited for watering my vegetable garden. Meanwhile, golf courses remained green with permits.",
            "Water restrictions banned washing cars but ignored leaky city infrastructure that wastes 30% of supply through broken pipes.",
            "Tiered pricing in my city works better than rationing. High users pay premium rates while basic needs remain affordable."
        ],
        "reasoning_A": [
            "Significant usage reductions show mandatory restrictions achieve conservation goals that voluntary measures cannot accomplish.",
            "Differential outcomes between restricted and unrestricted areas prove conservation policies can prevent infrastructure failure.",
            "Crisis avoidance demonstrates water rationing can be essential for maintaining basic services during severe shortages."
        ],
        "reasoning_B": [
            "Unequal enforcement shows water restrictions can unfairly target small users while exempting major consumers.",
            "Infrastructure waste indicates restrictions may address symptoms rather than underlying causes of water system inefficiency.",
            "Pricing success suggests market-based approaches can achieve conservation goals more fairly than command-and-control rationing."
        ],
        "category": "environment"
    },
    {
        "id": "pesticide_restrictions",
        "probe": "Should governments ban widely-used pesticides that may harm pollinators?",
        "stance_A": "Yes, we must ban neonicotinoid pesticides to save bee populations that are essential for food production. I keep honeybees and have watched colonies collapse near treated cornfields. European countries banned these chemicals and bee populations are recovering. One-third of our food depends on pollination - protecting bees is protecting our food security.",
        "stance_B": "No, pesticide bans would devastate crop yields and increase food costs while benefits are uncertain. I farm 2,000 acres and neonicotinoids are crucial for protecting seed germination from soil pests. Alternative treatments are less effective and more expensive. Many factors affect bee health beyond pesticides - banning effective tools hurts farmers without solving the real problems.",
        "experiences_A": [
            "My bee colonies near organic farms thrive while those near conventional corn show higher mortality and abnormal behavior patterns.",
            "France's neonicotinoid ban led to wild bee population increases. Biodiversity surveys show recovery of native pollinator species.",
            "I switched to organic apple production after seeing pesticides kill beneficial insects. Natural pest control works with proper management."
        ],
        "experiences_B": [
            "When Ontario restricted neonicotinoids, my corn yields dropped 15% from wireworm damage. Alternative treatments cost twice as much.",
            "European farmers are struggling with pest outbreaks after neonicotinoid bans. Some are requesting emergency use permits for banned chemicals.",
            "Varroa mites and viruses are the main threats to my bee colonies, not pesticides. Focusing on chemicals ignores the real causes of decline."
        ],
        "reasoning_A": [
            "Colony health differences between organic and conventional areas suggest pesticides are a significant factor in bee mortality.",
            "Population recovery after bans provides evidence that removing these pesticides can restore pollinator ecosystems.",
            "Successful organic transition shows alternative pest management approaches can maintain productivity without harmful chemicals."
        ],
        "reasoning_B": [
            "Yield losses and increased costs demonstrate pesticide restrictions can significantly impact agricultural productivity and farmer economics.",
            "European struggles with pest outbreaks show bans can create new agricultural problems that may require continued chemical intervention.",
            "Alternative causes of bee decline suggest pesticide bans may not address the primary factors affecting pollinator health."
        ],
        "category": "environment"
    },
    {
        "id": "organic_food_worth_cost",
        "probe": "Should people spend extra money on organic food?",
        "stance_A": "Yes, organic food is absolutely worth the extra cost. My family switched to organic five years ago and our health dramatically improved - fewer colds, better energy, and my son's eczema completely cleared up. I can taste the difference in organic produce, and knowing we're avoiding pesticides and supporting sustainable farming practices makes every extra dollar worthwhile. The long-term health savings will far outweigh the grocery costs.",
        "stance_B": "No, organic food is mostly marketing hype that wastes money. I compared organic and conventional produce for a year - same nutritional content, same taste, but 40% higher cost. My family eats plenty of conventional fruits and vegetables and we're perfectly healthy. The pesticide residues on conventional food are well within safe limits, and I'd rather spend that extra money on more variety of regular produce.",
        "experiences_A": [
            "My son's severe eczema cleared up within 3 months of switching to organic dairy and produce. His pediatrician was amazed.",
            "I can absolutely taste the difference - organic strawberries are so much sweeter and tomatoes actually taste like tomatoes.",
            "Our family gets sick way less often since going organic. We used to catch every cold, now maybe one per year."
        ],
        "experiences_B": [
            "I did a blind taste test with organic vs conventional apples and carrots. Couldn't tell the difference 8 out of 10 times.",
            "My grocery bills went up 40% when I tried organic for 6 months. Same nutritional content according to my dietitian.",
            "My kids are perfectly healthy eating conventional produce. My pediatrician said pesticide residues are negligible and safe."
        ],
        "reasoning_A": [
            "Dramatic eczema improvement suggests removing pesticide exposure can resolve inflammatory conditions.",
            "Taste differences indicate organic farming may preserve more natural compounds and flavors.",
            "Reduced illness frequency could indicate fewer chemical exposures supporting better immune function."
        ],
        "reasoning_B": [
            "Inability to detect taste differences in blind testing shows perceived benefits may be psychological.",
            "Professional nutritional guidance confirming equivalent content questions the value proposition.",
            "Medical professionals confirming safety standards suggests organic premiums aren't medically necessary."
        ],
        "category": "health"
    },
    {
        "id": "screen_time_limits_adults",
        "probe": "Should adults actively limit their daily screen time?",
        "stance_A": "Yes, adults absolutely need to limit screen time just like kids do. I was spending 8+ hours daily on devices and developed chronic neck pain, eye strain, and terrible sleep. Since setting strict limits - no phones after 8pm, one hour maximum social media - my sleep improved dramatically and I'm much more present with my family. My productivity actually increased because I stopped mindless scrolling. Screen addiction is real and destroying our mental health.",
        "stance_B": "No, adults can self-regulate and don't need artificial limits. I use screens 10+ hours daily for work and entertainment, but I'm intentional about it - reading articles, video calls with friends, creative projects. Setting arbitrary limits made me anxious and restricted legitimate uses. My eye doctor says my vision is fine, I sleep well, and screens enable my career and social connections. Quality of screen use matters more than quantity.",
        "experiences_A": [
            "I was getting chronic headaches and neck pain from 8+ hours of screen time daily. Limiting to 4 hours eliminated both issues completely.",
            "My sleep was terrible until I banned phones after 8pm. Now I fall asleep in 10 minutes instead of lying awake scrolling.",
            "I started reading actual books again after limiting screens. Finished 12 books this year vs zero last year."
        ],
        "experiences_B": [
            "I use screens 12+ hours daily for design work and stay connected with friends overseas. Setting limits would hurt my career and relationships.",
            "I tried screen time apps for 3 months and they just made me anxious. I'd watch the timer instead of focusing on quality content.",
            "My eye doctor said my vision is perfect despite heavy computer use. I take breaks and use good lighting - that matters more than time limits."
        ],
        "reasoning_A": [
            "Physical symptoms resolving with reduced usage demonstrates measurable health impacts from excessive screen time.",
            "Sleep improvement shows screen light and mental stimulation directly interfere with circadian rhythms.",
            "Returning to offline activities indicates screens were crowding out other beneficial behaviors."
        ],
        "reasoning_B": [
            "Professional and social benefits show screens can be essential tools rather than just entertainment.",
            "Anxiety from monitoring suggests artificial limits can create more stress than they prevent.",
            "Medical clearance with proper ergonomics shows technique and quality matter more than duration."
        ],
        "category": "health"
    },
    {
        "id": "sugar_elimination_diet",
        "probe": "Should people eliminate added sugar from their diet completely?",
        "stance_A": "Yes, eliminating added sugar is one of the best decisions I've made for my health. After cutting out all added sugars for six months, my energy levels stabilized completely - no more afternoon crashes. I lost 25 pounds without changing anything else, my skin cleared up, and my cravings for sweets disappeared entirely. Sugar is genuinely addictive and inflammatory. Natural sugars from fruit provide everything you need without the metabolic chaos.",
        "stance_B": "No, complete sugar elimination is unnecessary and unsustainable for most people. I tried cutting all added sugar for four months and became obsessed with reading every label, stressed at social events, and developed an unhealthy fear of food. Moderate sugar intake - maybe 25g daily - works perfectly fine. My energy is stable, my weight is healthy, and I can enjoy birthday cake without guilt or binge eating.",
        "experiences_A": [
            "I eliminated all added sugar 8 months ago and my afternoon energy crashes completely disappeared. I used to need coffee at 3pm daily.",
            "My adult acne cleared up within 6 weeks of going sugar-free. My dermatologist was shocked at the improvement.",
            "I lost 25 pounds in 4 months without changing portion sizes or exercise, just cutting added sugar from my diet."
        ],
        "experiences_B": [
            "I tried zero added sugar for 4 months and became obsessed with reading every single food label. It created more stress than benefits.",
            "At social events I'd either break my sugar rule and binge eat dessert, or sit there anxiously avoiding everything. Neither felt healthy.",
            "I maintain steady energy and healthy weight with moderate sugar intake - maybe a small dessert daily. Balance works better than extremes."
        ],
        "reasoning_A": [
            "Stable energy throughout the day indicates sugar was causing blood glucose spikes and crashes.",
            "Skin improvement suggests added sugar was triggering inflammatory responses in the body.",
            "Effortless weight loss shows sugar was driving excess calorie consumption and metabolic dysfunction."
        ],
        "reasoning_B": [
            "Obsessive label-reading behavior indicates complete elimination can trigger disordered eating patterns.",
            "Social anxiety around food shows extreme restrictions can harm psychological and social wellbeing.",
            "Maintaining health with moderation proves complete elimination isn't necessary for most people."
        ],
        "category": "health"
    },
    {
        "id": "alternative_medicine_integration",
        "probe": "Should people integrate alternative medicine with conventional treatment?",
        "stance_A": "Yes, integrating alternative medicine with conventional treatment gives the best outcomes. When I was diagnosed with chronic pain, combining physical therapy with acupuncture and meditation worked far better than pills alone. My oncologist actually recommended we add turmeric supplements and yoga during my cancer treatment - my side effects were much milder than expected. Alternative approaches address the whole person, not just symptoms, and often have fewer side effects than pharmaceuticals.",
        "stance_B": "No, alternative medicine can interfere with real treatment and waste precious time. My aunt delayed chemotherapy for three months trying herbal remedies and her cancer progressed significantly. I spent thousands on naturopaths for my autoimmune condition before finally seeing a rheumatologist who fixed it with proper medication in weeks. Alternative medicine lacks rigorous testing and can give false hope when people need proven treatments.",
        "experiences_A": [
            "My oncologist recommended adding turmeric and yoga to chemotherapy. My nausea and fatigue were much milder than other patients experienced.",
            "Chronic back pain improved dramatically when I combined physical therapy with weekly acupuncture sessions. Neither worked well alone.",
            "My anxiety medication worked better when I added meditation and herbal teas. The combination let me reduce my dosage by half."
        ],
        "experiences_B": [
            "My aunt tried herbal cancer treatments for 3 months before chemo. Her tumor grew 40% and treatment became much more aggressive.",
            "I wasted 2 years and $3000 on naturopaths for joint pain. One rheumatology visit and proper medication solved it in weeks.",
            "My friend's diabetes got dangerous when she reduced insulin to try 'natural' blood sugar control. She ended up hospitalized."
        ],
        "reasoning_A": [
            "Medical professional endorsement shows integration can be evidence-based rather than replacing conventional care.",
            "Synergistic effects demonstrate alternative therapies can enhance conventional treatment effectiveness.",
            "Reduced medication needs with maintained efficacy suggests alternative approaches can minimize pharmaceutical side effects."
        ],
        "reasoning_B": [
            "Disease progression during alternative treatment shows delays can have serious medical consequences.",
            "Rapid conventional treatment success after alternative failure demonstrates the superiority of evidence-based medicine.",
            "Hospitalization from reducing proven treatment shows alternative approaches can be genuinely dangerous."
        ],
        "category": "health"
    },
    {
        "id": "fitness_tracking_devices",
        "probe": "Should people use fitness tracking devices to monitor their health?",
        "stance_A": "Yes, fitness trackers are incredibly valuable for health monitoring. My Apple Watch detected an irregular heartbeat that led to diagnosing atrial fibrillation - my doctor said it likely prevented a stroke. Tracking my steps motivated me to walk 10,000 daily, I lost 20 pounds, and seeing my sleep patterns helped me realize I needed better sleep hygiene. The data doesn't lie and having objective metrics keeps me accountable to my health goals.",
        "stance_B": "No, fitness trackers create obsessive behavior and aren't medically reliable. I wore a Fitbit for two years and became anxious when I couldn't hit arbitrary step goals, even when I was genuinely tired or had other commitments. The heart rate readings were often wrong, and I started ignoring my body's signals in favor of what the device said. I'm much healthier now listening to my body rather than chasing meaningless numbers.",
        "experiences_A": [
            "My smartwatch detected irregular heart rhythm during a normal day. Turned out I had atrial fibrillation and needed medication.",
            "Tracking steps motivated me to park farther away and take stairs. I hit 10,000 steps daily and lost 20 pounds over 6 months.",
            "Sleep tracking showed I was only getting 4-5 hours of deep sleep. Changed my routine and now feel much more rested."
        ],
        "experiences_B": [
            "I became obsessed with hitting 10,000 steps even when exhausted from work. Ended up with stress fractures from overwalking.",
            "My fitness tracker said my heart rate was dangerous during exercise, but my doctor said the readings were completely inaccurate.",
            "I stopped listening to hunger cues and ate based on what my tracker said I 'burned.' Developed really unhealthy eating patterns."
        ],
        "reasoning_A": [
            "Early medical detection shows wearable devices can identify serious conditions before symptoms appear.",
            "Behavioral motivation from tracking demonstrates objective data can drive positive lifestyle changes.",
            "Sleep pattern insights provide actionable data that subjective feelings might miss."
        ],
        "reasoning_B": [
            "Exercise-related injuries show goal obsession can override important physical warning signals.",
            "Inaccurate medical readings demonstrate consumer devices aren't reliable for health decisions.",
            "Disrupted eating patterns indicate tracking can interfere with natural body regulation mechanisms."
        ],
        "category": "health"
    },
    {
        "id": "vitamin_supplements_healthy_adults",
        "probe": "Should healthy adults take daily vitamin supplements?",
        "stance_A": "Yes, vitamin supplements are essential even for healthy adults. I started taking a high-quality multivitamin plus D3 and B12 three years ago and my energy levels increased dramatically. My annual blood work shows optimal levels of everything now, whereas before I was deficient in several areas despite eating well. Modern soil depletion and food processing mean we can't get adequate nutrition from food alone. My immune system is stronger - I haven't had a cold in two years.",
        "stance_B": "No, healthy adults with good diets don't need vitamin supplements. I took expensive multivitamins for five years and my blood work showed no difference compared to now when I eat a varied diet without supplements. Most vitamins just create expensive urine, and some can actually be harmful in high doses. My doctor said my nutrition is perfect from food alone, and I save $100+ monthly by not buying unnecessary pills.",
        "experiences_A": [
            "My blood work showed I was deficient in D3, B12, and iron despite eating well. Supplements brought everything to optimal levels.",
            "I used to get 3-4 colds per year. Since starting vitamins 2 years ago, I haven't been sick once.",
            "My energy crashed every afternoon until I started B-complex vitamins. Now I maintain steady energy all day without caffeine."
        ],
        "experiences_B": [
            "I compared blood work after 5 years of expensive supplements vs eating varied foods. No difference in any vitamin levels.",
            "My doctor said my nutrition panels are perfect just from diet. I'm wasting money on supplements my body doesn't need.",
            "I took high-dose vitamin A and E for years until learning they can increase cancer risk. Food sources are much safer."
        ],
        "reasoning_A": [
            "Blood test improvements demonstrate supplements can correct deficiencies that diet alone cannot address.",
            "Reduced illness frequency suggests optimal vitamin levels strengthen immune system function.",
            "Energy stabilization indicates B-vitamins were addressing a metabolic need not met by food intake."
        ],
        "reasoning_B": [
            "Identical blood work with and without supplements proves a good diet provides adequate nutrition.",
            "Medical professional confirmation shows food-based nutrition can meet all requirements without supplementation.",
            "Cancer risk from high-dose vitamins demonstrates supplements can exceed safe levels unlike food sources."
        ],
        "category": "health"
    },
    {
        "id": "standing_desk_benefits",
        "probe": "Should office workers use standing desks to improve their health?",
        "stance_A": "Yes, standing desks are a game-changer for office worker health. I switched to a standing desk two years ago and my chronic lower back pain completely disappeared within weeks. My posture improved dramatically, I have more energy throughout the day, and I naturally move more instead of being glued to my chair. My productivity actually increased because I feel more alert and engaged. The research on sitting disease is clear - prolonged sitting is genuinely harmful.",
        "stance_B": "No, standing desks create more problems than they solve for most people. I tried a standing desk for eight months and developed severe foot pain, varicose veins, and constant fatigue. Standing all day is just as bad as sitting all day - the key is movement and variation. I'm much more comfortable and productive with a regular desk where I can sit properly and take walking breaks every hour.",
        "experiences_A": [
            "My chronic lower back pain from 10 years of desk work disappeared within 3 weeks of switching to a standing desk.",
            "I naturally fidget and shift positions while standing, which keeps me more alert than when I was sedentary in a chair.",
            "My posture improved dramatically - no more hunched shoulders and forward head position that caused neck strain."
        ],
        "experiences_B": [
            "After 6 months with a standing desk, I developed plantar fasciitis and severe foot pain that required physical therapy.",
            "I was constantly exhausted by 2pm from standing all day. My productivity dropped because I couldn't focus through the discomfort.",
            "I developed visible varicose veins in my legs from prolonged standing that my doctor said were from the desk setup."
        ],
        "reasoning_A": [
            "Back pain resolution shows standing corrects spinal alignment issues caused by prolonged sitting.",
            "Increased natural movement indicates standing promotes beneficial micro-movements throughout the workday.",
            "Posture improvements demonstrate standing prevents the forward head and rounded shoulder positioning from chairs."
        ],
        "reasoning_B": [
            "Foot injuries show standing creates new stress points and overuse problems in the lower extremities.",
            "Fatigue and productivity decline indicate prolonged standing causes its own form of physical stress.",
            "Vascular problems demonstrate standing can impede circulation and create new health complications."
        ],
        "category": "health"
    },
    {
        "id": "meditation_mental_health",
        "probe": "Should people practice daily meditation for mental health benefits?",
        "stance_A": "Yes, daily meditation is absolutely essential for mental health. I started meditating 10 minutes every morning two years ago and it transformed my anxiety and stress levels completely. My reaction to difficult situations is so much calmer now, I sleep better, and I feel more emotionally resilient overall. Even my therapist noticed how much more self-aware and grounded I've become. It's like exercise for your mind - the benefits compound over time.",
        "stance_B": "No, meditation isn't for everyone and can actually worsen some mental health conditions. I tried daily meditation for six months and it made my anxiety worse - sitting alone with my thoughts was torture. The pressure to 'clear my mind' created more stress, and I felt like a failure when I couldn't focus. I'm much better with active stress relief like running or socializing. Meditation works for some people but it's not a universal solution.",
        "experiences_A": [
            "I used to have panic attacks weekly. After 6 months of daily meditation, I haven't had one in over a year.",
            "My therapist said I'm much more self-aware and emotionally regulated since starting meditation. I catch negative thought spirals earlier.",
            "I sleep through the night now instead of waking up anxious at 3am. Meditation taught me to quiet my racing mind."
        ],
        "experiences_B": [
            "Daily meditation made my anxiety worse - sitting alone with racing thoughts felt like torture. I'd end sessions more stressed than when I started.",
            "The pressure to 'succeed' at meditation created more stress. I felt like a failure when my mind wandered constantly.",
            "I tried guided meditation apps for 4 months but preferred running or calling friends. Active stress relief works better for my personality."
        ],
        "reasoning_A": [
            "Panic attack elimination demonstrates meditation can regulate the nervous system's stress response.",
            "Professional observation of improved emotional regulation shows meditation develops genuine psychological skills.",
            "Sleep improvements indicate meditation helps calm mental hyperactivity that interferes with rest."
        ],
        "reasoning_B": [
            "Increased anxiety shows meditation can amplify rather than calm mental distress for some individuals.",
            "Performance pressure around meditation can create additional stress rather than providing relief.",
            "Better results with alternative activities proves different personality types need different stress management approaches."
        ],
        "category": "health"
    },
    {
        "id": "fitness_tracking",
        "probe": "Should people track their daily fitness metrics (steps, calories, heart rate)?",
        "stance_A": "Yes, tracking fitness metrics is essential for health improvement. I've been using a fitness tracker for three years and it completely transformed my activity levels - I went from sedentary to walking 12,000 steps daily just because I could see the numbers. The data helped me identify patterns, set realistic goals, and stay motivated when I could see concrete progress over time.",
        "stance_B": "No, fitness tracking creates unhealthy obsession and stress. I used a fitness tracker for two years and it made me anxious about hitting arbitrary daily targets, even when I was sick or needed rest. The constant monitoring turned exercise from something enjoyable into a chore driven by guilt and numbers rather than how my body actually felt.",
        "experiences_A": [
            "I started tracking steps and went from 3,000 to 12,000 daily steps within months. The visual feedback was incredibly motivating.",
            "My heart rate monitor helped me discover I wasn't working hard enough during cardio. I improved my fitness significantly.",
            "Tracking sleep patterns showed me I needed more rest on workout days. My recovery improved dramatically."
        ],
        "experiences_B": [
            "I became obsessed with closing my activity rings even when sick. It created unhealthy pressure and guilt.",
            "My tracker said I burned 300 calories but the gym machine said 450. The inconsistency made me distrust all the data.",
            "I stopped enjoying hikes because I was constantly checking my watch instead of appreciating nature."
        ],
        "reasoning_A": [
            "Concrete data visualization provided immediate feedback that motivated sustained behavioral change.",
            "Objective metrics revealed training inefficiencies that subjective feelings couldn't identify.",
            "Sleep tracking data enabled evidence-based recovery optimization that improved performance."
        ],
        "reasoning_B": [
            "The compulsive behavior shows tracking can override natural body signals and create unhealthy relationships with exercise.",
            "Inconsistent measurements demonstrate the unreliability of consumer-grade tracking technology.",
            "The distraction from present-moment experience shows tracking can diminish intrinsic motivation for physical activity."
        ],
        "category": "health"
    },
    {
        "id": "supplement_multivitamins",
        "probe": "Should healthy adults take daily multivitamin supplements?",
        "stance_A": "Yes, multivitamins provide valuable nutritional insurance for most people. I've taken a high-quality multivitamin for five years and my annual blood work consistently shows optimal levels of key nutrients, while my friends who don't supplement often have deficiencies. Even with a good diet, it's nearly impossible to get perfect nutrition from food alone, especially with soil depletion and modern farming practices.",
        "stance_B": "No, multivitamins are unnecessary for people eating a balanced diet and may even be harmful. I stopped taking multivitamins after my doctor found my iron and vitamin A levels were too high, which can increase health risks. Most people can get all nutrients from whole foods, and studies show multivitamins don't reduce disease risk or improve health outcomes in healthy populations.",
        "experiences_A": [
            "I've taken multivitamins for five years and my blood work always shows optimal nutrient levels. My unsupplemented friends often have deficiencies.",
            "During a busy period eating poorly, my multivitamin helped maintain my energy and prevented getting sick like my coworkers.",
            "My doctor recommended a multivitamin after finding I was low in several nutrients despite trying to eat well."
        ],
        "experiences_B": [
            "My doctor found my iron and vitamin A levels were dangerously high from multivitamins. I had to stop taking them immediately.",
            "I felt no difference when I stopped my daily multivitamin after two years. My energy and health remained exactly the same.",
            "A nutritionist showed me how my normal diet already provided most vitamins I was supplementing unnecessarily."
        ],
        "reasoning_A": [
            "Consistent optimal blood levels demonstrate that supplementation successfully prevents nutrient deficiencies.",
            "Maintained health during poor eating periods shows multivitamins can provide nutritional backup during stress.",
            "Medical recommendation based on testing indicates even conscious eaters may have gaps in nutrition."
        ],
        "reasoning_B": [
            "Dangerously high nutrient levels prove that supplementation can cause harmful overaccumulation of fat-soluble vitamins.",
            "No felt difference upon discontinuation suggests multivitamins provided no measurable health benefit.",
            "Professional dietary analysis revealed redundant supplementation, indicating most people already get sufficient nutrients from food."
        ],
        "category": "health"
    },
    {
        "id": "alternative_medicine",
        "probe": "Should people consider alternative medicine treatments (acupuncture, herbal remedies, chiropractic) alongside conventional healthcare?",
        "stance_A": "Yes, alternative medicine can provide valuable complementary benefits when used thoughtfully alongside conventional care. I've found acupuncture incredibly effective for chronic pain that physical therapy and medications couldn't touch, and my doctor now refers patients there regularly. Many traditional remedies have been used safely for centuries and can address root causes that conventional medicine sometimes misses.",
        "stance_B": "No, alternative medicine lacks scientific evidence and can delay or interfere with proven treatments. I wasted months and hundreds of dollars on herbal supplements and chiropractic care for back pain that only resolved with proper physical therapy based on evidence. Alternative practitioners often make unsupported claims and can even be dangerous when they discourage people from seeking real medical care.",
        "experiences_A": [
            "Acupuncture eliminated my chronic neck pain after physical therapy and painkillers failed. My doctor now refers patients there regularly.",
            "Herbal supplements helped my digestive issues when conventional treatments caused unpleasant side effects.",
            "My chiropractor identified postural problems that my regular doctor missed, leading to effective treatment."
        ],
        "experiences_B": [
            "I spent months on expensive herbal supplements and chiropractic care for back pain. Only evidence-based physical therapy actually helped.",
            "My naturopath told me to stop my thyroid medication and try supplements instead. My symptoms got much worse.",
            "Acupuncture did nothing for my migraines despite trying for three months. Prescription medication worked immediately."
        ],
        "reasoning_A": [
            "Success where conventional treatments failed demonstrates alternative approaches can address conditions through different therapeutic mechanisms.",
            "Medical professional referrals indicate growing integration of evidence-based alternative treatments into mainstream healthcare.",
            "Identifying missed diagnoses shows alternative practitioners may offer different diagnostic perspectives and examination methods."
        ],
        "reasoning_B": [
            "The contrast between failed alternative treatments and successful evidence-based therapy demonstrates the importance of scientific validation.",
            "Advice to discontinue proven medical treatments shows some alternative practitioners can provide dangerous medical guidance.",
            "Immediate prescription success after failed alternative treatment highlights the superior efficacy of scientifically-tested interventions."
        ],
        "category": "health"
    },
    {
        "id": "genetic_testing_health",
        "probe": "Should healthy people get genetic testing to assess their disease risks?",
        "stance_A": "Yes, genetic testing provides valuable information for preventive healthcare planning. I discovered through testing that I carry BRCA mutations and started enhanced screening protocols that caught my sister's breast cancer early when it was highly treatable. The information helped me make informed decisions about my health monitoring and allowed my family to take proactive steps based on our shared genetic risks.",
        "stance_B": "No, genetic testing creates unnecessary anxiety and discrimination risks without clear benefits for most people. I got tested and learned I have elevated Alzheimer's risk, which has caused me constant worry for three years without any proven prevention strategies available. The information affects my insurance decisions and mental health negatively while providing no actionable medical benefits.",
        "experiences_A": [
            "My genetic test revealed BRCA mutations. Enhanced screening caught my sister's breast cancer early when it was easily treatable.",
            "I learned I metabolize certain medications poorly, so my doctor adjusted my prescriptions accordingly with better results.",
            "Finding out about my cardiac risk factors motivated me to change my lifestyle proactively in my thirties."
        ],
        "experiences_B": [
            "I learned I have high Alzheimer's risk but there's no proven prevention. It's caused three years of constant anxiety.",
            "My genetic results showed diabetes risk, but my doctor said the same lifestyle advice applies to everyone anyway.",
            "I worry about genetic discrimination and avoid certain insurance products because of my test results."
        ],
        "reasoning_A": [
            "Early cancer detection through targeted screening demonstrates how genetic information can directly improve medical outcomes through personalized healthcare.",
            "Medication optimization based on genetic variants shows practical clinical applications that improve treatment effectiveness and reduce adverse reactions.",
            "Proactive lifestyle changes motivated by genetic risk information can prevent disease development before symptoms appear."
        ],
        "reasoning_B": [
            "Anxiety about untreatable conditions demonstrates how genetic knowledge can harm mental health without providing therapeutic benefit.",
            "Generic lifestyle recommendations regardless of genetic risk suggest testing doesn't change medical management for most conditions.",
            "Discrimination concerns show genetic information can create practical life disadvantages that outweigh potential medical benefits."
        ],
        "category": "health"
    },
    {
        "id": "screen_time_limits",
        "probe": "Should adults actively limit their daily screen time for better health?",
        "stance_A": "Yes, limiting screen time significantly improves physical and mental health. I implemented a strict 2-hour recreational screen limit six months ago and my sleep quality improved dramatically, my eye strain disappeared, and I have much better focus at work. I also started exercising more and socializing in person instead of scrolling mindlessly, which has made me feel more energetic and connected.",
        "stance_B": "No, arbitrary screen time limits are unrealistic in our digital world and can create unnecessary stress. I tried limiting screens but it made me anxious about checking important work emails and staying connected with distant family members who I primarily communicate with online. My screen use includes educational content, work productivity, and meaningful social connections that benefit my life and career.",
        "experiences_A": [
            "I limited recreational screen time to 2 hours daily. My sleep improved dramatically and eye strain disappeared completely.",
            "Reducing screen time led me to exercise more and socialize in person. I feel much more energetic and connected.",
            "My focus and productivity at work increased significantly after cutting evening screen use and improving sleep quality."
        ],
        "experiences_B": [
            "Screen time limits made me anxious about missing important work emails and staying connected with distant family members.",
            "Much of my screen time is educational content and work productivity. Blanket limits seemed counterproductive to my goals.",
            "I tried screen limits but the stress of monitoring and restricting myself was worse than my original usage patterns."
        ],
        "reasoning_A": [
            "Improved sleep and reduced eye strain demonstrate direct physical health benefits from decreased screen exposure.",
            "Increased physical activity and in-person social connection show screen reduction creates space for healthier behaviors.",
            "Enhanced work focus indicates that recreational screen time was interfering with cognitive performance and sleep recovery."
        ],
        "reasoning_B": [
            "Anxiety about missing communications shows screen limits can interfere with important social and professional responsibilities.",
            "Educational and productive screen use demonstrates that not all screen time is equivalent in terms of health impact.",
            "The stress of restriction itself became a health problem, indicating that rigid limits may cause more harm than benefit."
        ],
        "category": "health"
    },
    {
        "id": "preventive_medical_screening",
        "probe": "Should healthy adults get comprehensive annual medical screenings and tests?",
        "stance_A": "Yes, comprehensive annual screenings are essential for catching health issues early. My routine blood work three years ago detected pre-diabetes when I felt completely healthy, allowing me to make lifestyle changes that prevented full diabetes development. My friend's mammogram caught breast cancer at stage 1 with no symptoms, and early detection made treatment much more successful with better outcomes.",
        "stance_B": "No, excessive screening leads to overdiagnosis, unnecessary procedures, and healthcare anxiety without improving outcomes. I had an abnormal mammogram that led to six months of biopsies, stress, and medical appointments, only to find it was benign tissue that required no treatment. Many screening tests have high false positive rates that create medical trauma and expensive follow-ups for healthy people.",
        "experiences_A": [
            "My routine blood work detected pre-diabetes when I felt fine. Early intervention prevented me from developing full diabetes.",
            "My friend's screening mammogram caught stage 1 breast cancer with no symptoms. Early treatment was highly successful.",
            "Annual physicals caught my high blood pressure before I had any symptoms. Medication prevented stroke risk."
        ],
        "experiences_B": [
            "An abnormal mammogram led to six months of biopsies and anxiety, only to find benign tissue needing no treatment.",
            "My 'abnormal' cholesterol reading led to expensive cardiac tests, but my doctor said my levels were actually fine for my age.",
            "I developed medical anxiety from yearly screenings constantly looking for problems. It made me worry about my health unnecessarily."
        ],
        "reasoning_A": [
            "Early detection of pre-diabetes enabled preventive lifestyle interventions that avoided disease progression and complications.",
            "Asymptomatic cancer detection through screening allowed for more effective treatment with better survival outcomes.",
            "Pre-symptom blood pressure detection enabled medical management that prevented serious cardiovascular events."
        ],
        "reasoning_B": [
            "The false positive mammogram demonstrates how screening can cause significant psychological distress and unnecessary medical procedures.",
            "Misinterpretation of normal age-related changes shows screening can lead to expensive overtreatment of non-pathological conditions.",
            "Developing medical anxiety illustrates how frequent screening can harm mental health by creating excessive focus on potential illness."
        ],
        "category": "health"
    },
    {
        "id": "organic_food_health",
        "probe": "Should people prioritize buying organic foods for better health outcomes?",
        "stance_A": "Yes, organic foods provide significant health benefits worth the extra cost. I switched to primarily organic produce two years ago and noticed my digestive issues improved dramatically, likely due to reduced pesticide exposure. My children also have fewer allergic reactions since we went organic, and I feel better knowing we're avoiding synthetic chemicals that accumulate in the body over time.",
        "stance_B": "No, organic foods offer no meaningful health advantages and the premium price isn't justified. I ate organic for three years but saw no difference in how I felt, and studies show conventional produce is just as nutritious with negligible pesticide residues. The money I saved switching back to conventional allowed me to buy more fruits and vegetables overall, which probably benefits my health more than expensive organic options.",
        "experiences_A": [
            "I switched to organic produce two years ago and my chronic digestive issues improved significantly after the change.",
            "My children have fewer allergic reactions and skin problems since we started buying organic foods exclusively.",
            "I feel more energetic eating organic and worry less about chemical exposure accumulating in my body over time."
        ],
        "experiences_B": [
            "I ate organic for three years but felt no different. Studies show conventional produce has the same nutrition with minimal pesticides.",
            "The money I saved buying conventional allowed me to purchase more fruits and vegetables overall for better health.",
            "My doctor said there's no evidence organic foods provide health benefits beyond what conventional foods offer."
        ],
        "reasoning_A": [
            "Improved digestive health after switching suggests reduced pesticide exposure may benefit gut microbiome and digestive function.",
            "Fewer allergic reactions in children indicates organic foods may reduce exposure to synthetic chemicals that trigger immune responses.",
            "Increased energy and reduced chemical concerns demonstrate both physical and psychological health benefits from organic consumption."
        ],
        "reasoning_B": [
            "No felt difference combined with research findings indicates organic foods don't provide superior nutrition or measurable health improvements.",
            "Increased overall produce consumption from cost savings shows budget allocation toward quantity may outweigh organic quality benefits.",
            "Medical professional assessment confirms lack of evidence for organic health advantages, suggesting premium costs aren't medically justified."
        ],
        "category": "health"
    },
    {
        "id": "exercise_intensity_daily",
        "probe": "Should people prioritize high-intensity workouts over moderate daily activity for optimal health?",
        "stance_A": "Yes, high-intensity workouts provide superior health benefits in less time. I switched from daily walks to three HIIT sessions per week and saw dramatic improvements in my cardiovascular fitness, strength, and body composition within months. The intense workouts boost my metabolism for hours afterward and fit better into my busy schedule while delivering measurable results that moderate exercise never achieved.",
        "stance_B": "No, moderate daily activity is more sustainable and beneficial for long-term health. I tried high-intensity programs multiple times but always burned out or got injured within a few months, then became completely sedentary. Daily moderate exercise like walking and light strength training has kept me consistently active for years, improved my sleep and mood, and feels much more natural and enjoyable.",
        "experiences_B": [
            "I tried multiple HIIT programs but always burned out or got injured within months, then became completely sedentary.",
            "Daily walks and light strength training have kept me active consistently for five years with steady health improvements.",
            "High-intensity workouts left me exhausted and dreading exercise, while moderate activity energizes and motivates me daily."
        ],
        "experiences_A": [
            "I switched from daily walks to three HIIT sessions weekly. My cardiovascular fitness and body composition improved dramatically within months.",
            "High-intensity workouts boost my metabolism for hours and fit my busy schedule better than daily moderate exercise.",
            "My strength gains and endurance improvements were much faster with intense training than years of moderate activity."
        ],
        "reasoning_A": [
            "Dramatic fitness improvements demonstrate that high-intensity exercise provides superior physiological adaptations compared to moderate activity.",
            "Extended metabolic boost and time efficiency show HIIT delivers better health returns on time investment for busy lifestyles.",
            "Faster strength and endurance gains indicate intense training provides more effective stimulus for fitness development."
        ],
        "reasoning_B": [
            "Repeated burnout and injury patterns show high-intensity exercise is unsustainable and can lead to complete activity cessation.",
            "Five years of consistent moderate activity demonstrates that sustainability is more important than short-term intensity for long-term health.",
            "Positive psychological response to moderate exercise shows enjoyment and motivation are crucial for maintaining lifelong healthy habits."
        ],
        "category": "health"
    },
    {
        "id": "reproducibility_crisis",
        "probe": "Should journals require reproducibility verification before publication?",
        "stance_A": "Yes, reproducibility verification should be mandatory before any study is published. I've wasted months trying to replicate published experiments that contained critical missing steps or unreported parameters. Independent verification would catch these issues early and restore trust in scientific literature. The current system publishes too much unreproducible work.",
        "stance_B": "No, requiring reproducibility verification would slow science to a crawl and waste resources. I've seen important discoveries that couldn't be immediately reproduced due to rare materials or specialized techniques. Verification requirements would favor simple studies over breakthrough research. Post-publication replication is more efficient than pre-publication bottlenecks.",
        "experiences_A": [
            "I spent 6 months failing to replicate a protein synthesis method before discovering the authors omitted a crucial pH buffer step.",
            "Our lab tried to reproduce 12 psychology studies and succeeded with only 3 due to missing methodological details.",
            "I caught a major statistical error during verification that would have misled an entire research field."
        ],
        "experiences_B": [
            "My breakthrough imaging technique took 3 years to replicate because it required custom-built equipment and specific expertise.",
            "We delayed publishing life-saving cancer research for 8 months while other labs struggled with verification requirements.",
            "I've seen revolutionary discoveries dismissed because initial replication attempts failed due to technical skill differences."
        ],
        "reasoning_A": [
            "The missing buffer step shows how verification would catch methodological gaps that waste other researchers' time.",
            "The low replication rate demonstrates systematic problems in current publication standards.",
            "Statistical error detection proves verification prevents misinformation from entering the literature."
        ],
        "reasoning_B": [
            "The 3-year replication timeline shows some legitimate discoveries require specialized conditions.",
            "Publication delays for cancer research demonstrate how verification requirements could cost lives.",
            "Dismissed discoveries show verification requirements might suppress genuine innovations."
        ],
        "category": "science"
    },
    {
        "id": "citizen_science_validity",
        "probe": "Should citizen science contributions be given equal weight to professional research?",
        "stance_A": "Yes, citizen science produces valuable research that deserves equal consideration. I've seen amateur astronomers discover exoplanets and bird watchers provide climate data more comprehensive than any professional study. Citizen scientists often have more time for careful observation and bring fresh perspectives without academic biases. Quality should matter more than credentials.",
        "stance_B": "No, citizen science lacks the rigor and expertise necessary for reliable research. I've reviewed citizen data filled with identification errors and methodological problems that would mislead scientific conclusions. Professional training exists for good reasons - statistical analysis, experimental controls, and systematic bias recognition require years of education. Equal weight would lower scientific standards.",
        "experiences_A": [
            "Amateur astronomers in our network discovered 12 new asteroids using data that professionals overlooked.",
            "Citizen bird watchers provided 50,000 migration observations that revolutionized our climate models.",
            "I've seen hobbyist botanists identify plant species misclassified by university researchers for decades."
        ],
        "experiences_B": [
            "I processed citizen bird data where 30% of species identifications were completely wrong.",
            "Amateur weather stations in our network had systematic calibration errors that skewed temperature readings.",
            "I reviewed citizen health studies that ignored obvious confounding variables and drew invalid conclusions."
        ],
        "reasoning_A": [
            "Asteroid discoveries show citizen scientists can achieve results that professional oversight missed.",
            "The massive migration dataset demonstrates citizen science's unique capacity for large-scale data collection.",
            "Species corrections prove citizen expertise can sometimes exceed professional knowledge in specific domains."
        ],
        "reasoning_B": [
            "The 30% error rate shows citizen scientists lack training for accurate data collection.",
            "Calibration errors demonstrate technical expertise requirements that citizens often can't meet.",
            "Confounding variable ignorance proves statistical training is essential for valid research conclusions."
        ],
        "category": "science"
    },
    {
        "id": "preprint_reliability",
        "probe": "Should preprint servers require basic quality checks before posting?",
        "stance_A": "Yes, preprint servers need minimal quality standards to prevent misinformation spread. I've seen completely fabricated COVID studies go viral from preprint servers before any expert could debunk them. Basic checks for data availability, methodology description, and statistical coherence would filter obvious junk without slowing legitimate research. Current anything-goes policies damage scientific credibility.",
        "stance_B": "No, quality checks would defeat the purpose of preprint servers as rapid communication tools. I've used preprints to share urgent findings during disease outbreaks when peer review would take months. Any filtering system would introduce bias and delay important discoveries. The scientific community can evaluate quality better than automated gatekeepers.",
        "experiences_A": [
            "I saw a preprint claiming 5G towers cause COVID spread nationwide on social media before scientists could respond.",
            "We found a completely data-free preprint about cancer cures that gave false hope to desperate patients.",
            "I've seen preprints with basic statistical errors that undergraduate students would catch get cited in policy documents."
        ],
        "experiences_B": [
            "I shared critical Ebola research through preprints that reached health workers 6 months before journal publication.",
            "Our earthquake prediction model preprint helped emergency responders even though it hadn't passed peer review yet.",
            "I've seen important discoveries buried by overly strict editorial policies that preprints bypass."
        ],
        "reasoning_A": [
            "The 5G misinformation shows how unfiltered preprints can fuel dangerous conspiracy theories.",
            "Data-free cancer claims demonstrate how lack of basic standards harms vulnerable populations.",
            "Policy citation errors prove preprint quality problems have real-world consequences."
        ],
        "reasoning_B": [
            "Ebola research sharing shows preprints can save lives when time-sensitive information needs rapid dissemination.",
            "Emergency response applications demonstrate preprints' value for actionable science before formal publication.",
            "Editorial bias examples show quality checks can suppress legitimate research that challenges established views."
        ],
        "category": "science"
    },
    {
        "id": "science_funding_priorities",
        "probe": "Should basic research receive equal funding priority to applied research?",
        "stance_A": "Yes, basic research deserves equal funding because it drives long-term breakthroughs we can't predict. I've seen fundamental physics research lead to MRI machines and quantum computing applications decades later. Without curiosity-driven science, we only get incremental improvements on existing technology. History shows our biggest advances come from basic discoveries with no obvious applications.",
        "stance_B": "No, applied research addressing immediate human needs should get funding priority. I've worked on medical devices that save lives today using well-established scientific principles. Basic research is a luxury when people are dying from diseases we could cure with targeted applied research. Limited resources should focus on practical solutions to urgent problems.",
        "experiences_A": [
            "I studied seemingly useless butterfly wing patterns that led to new optical materials worth billions in solar panels.",
            "Our basic genetics research with no medical goal discovered mechanisms now used in cancer immunotherapy.",
            "I've seen applied projects fail repeatedly because the underlying basic science wasn't understood yet."
        ],
        "experiences_B": [
            "I developed a water purification system that prevents cholera in refugee camps using 20-year-old chemistry knowledge.",
            "Our applied AI research created diagnostic tools helping doctors in rural areas where basic research would be irrelevant.",
            "I've watched basic research consume millions while children die from diseases we know how to prevent."
        ],
        "reasoning_A": [
            "Butterfly research leading to solar technology shows unpredictable pathways from basic to applied science.",
            "Cancer therapy discovery demonstrates basic research creates entirely new treatment categories.",
            "Applied project failures show insufficient basic understanding limits practical progress."
        ],
        "reasoning_B": [
            "Water purification success shows applied research can immediately solve life-threatening problems with existing knowledge.",
            "Diagnostic tools prove targeted applied research addresses urgent healthcare inequities effectively.",
            "The contrast between research spending and preventable deaths highlights moral priorities in resource allocation."
        ],
        "category": "science"
    },
    {
        "id": "research_collaboration_competition",
        "probe": "Should scientific research prioritize collaboration over competition between labs?",
        "stance_A": "Yes, collaboration produces better science than competition between isolated labs. I've participated in multi-lab consortiums that solved problems no single group could handle alone. Sharing resources, expertise, and data accelerates discovery while reducing duplication of effort. Competitive secrecy wastes resources and slows progress on humanity's biggest challenges.",
        "stance_B": "No, competition drives scientific excellence and innovation better than collaboration. I've seen collaborative projects become slow, bureaucratic compromises that satisfy everyone but advance nothing. Competition motivates researchers to work harder, think more creatively, and challenge established ideas. Without competitive pressure, science becomes complacent and stagnant.",
        "experiences_A": [
            "Our 12-lab cancer consortium discovered new drug targets by combining datasets no single lab could generate.",
            "I've seen competitive labs waste years duplicating each other's failed experiments instead of sharing negative results.",
            "International climate collaboration gave us global models that competitive national efforts couldn't achieve."
        ],
        "experiences_B": [
            "I watched a 15-lab collaboration spend 3 years arguing about methodology while competitors published breakthrough results.",
            "Our lab's competitive drive to beat rivals led us to discover revolutionary gene editing techniques.",
            "I've seen collaborative projects produce bland consensus results that avoided challenging any existing theories."
        ],
        "reasoning_A": [
            "Combined datasets show collaboration enables research scale impossible for individual competitive labs.",
            "Duplicated failures demonstrate how competition wastes resources that collaboration would share efficiently.",
            "Global climate modeling proves some scientific problems require collaborative coordination beyond competitive capabilities."
        ],
        "reasoning_B": [
            "The 3-year delay shows collaborative bureaucracy can prevent timely scientific progress.",
            "Gene editing breakthroughs demonstrate competitive motivation drives major innovations.",
            "Bland consensus outcomes show collaboration can suppress bold hypotheses that advance knowledge."
        ],
        "category": "science"
    },
    {
        "id": "scientific_communication_public",
        "probe": "Should scientists be required to communicate their research in accessible public language?",
        "stance_A": "Yes, scientists have an obligation to make their work accessible to the taxpayers who fund it. I've seen important research buried in jargon while the public makes uninformed decisions about science policy. Clear communication builds trust, increases science literacy, and helps people make better choices about health and environment. Democracy requires informed citizens.",
        "stance_B": "No, forcing scientists to oversimplify complex research creates more misinformation than clarity. I've watched media distort carefully nuanced studies into misleading headlines that confuse the public more. Scientific precision requires technical language that can't be dumbed down without losing meaning. Public communication should be left to trained science communicators, not researchers.",
        "experiences_A": [
            "I started writing blog posts about my climate research and helped voters understand local environmental policies better.",
            "Our lab's public talks about vaccination research directly countered misinformation spreading in our community.",
            "I've seen important nutrition studies ignored by policymakers because the technical papers were incomprehensible."
        ],
        "experiences_B": [
            "Journalists turned my nuanced cancer study into 'Scientists Discover Miracle Cure' headlines that gave patients false hope.",
            "I spent more time on public outreach than research and my scientific productivity dropped significantly.",
            "We saw anti-vaccine activists quote simplified explanations out of context to support dangerous conspiracy theories."
        ],
        "reasoning_A": [
            "Improved voter understanding shows accessible communication enables better democratic decisions about science policy.",
            "Direct misinformation countering demonstrates scientists' unique authority and responsibility in public debates.",
            "Policy maker neglect proves technical language barriers prevent important research from influencing decisions."
        ],
        "reasoning_B": [
            "False miracle cure headlines show media translation introduces dangerous inaccuracies that mislead patients.",
            "Reduced productivity demonstrates communication requirements divert scientists from their primary research contributions.",
            "Conspiracy theory misuse shows simplified explanations provide ammunition for science deniers."
        ],
        "category": "science"
    },
    {
        "id": "research_ethics_oversight",
        "probe": "Should research ethics committees have more authority to halt ongoing studies?",
        "stance_A": "Yes, ethics committees need stronger enforcement power to protect research subjects and scientific integrity. I've seen studies continue despite clear evidence of harm because committees could only make recommendations. Stronger authority would prevent ethical violations that damage public trust in science. Researchers sometimes prioritize career advancement over participant welfare and need external oversight.",
        "stance_B": "No, giving ethics committees more authority would create bureaucratic barriers that slow important research. I've watched committees with no field expertise halt promising medical studies based on theoretical concerns rather than actual evidence. Researchers already follow strict ethical guidelines and additional oversight would discourage innovative studies that could save lives.",
        "experiences_A": [
            "I reported a psychology study causing obvious participant distress, but it continued for 6 months because the committee had no enforcement power.",
            "Our ethics review caught a drug trial with inadequate safety monitoring that could have killed patients.",
            "I've seen researchers ignore committee recommendations because compliance was voluntary rather than mandatory."
        ],
        "experiences_B": [
            "An ethics committee halted our Alzheimer's trial based on paperwork concerns while patients desperately needed the experimental treatment.",
            "I watched a committee with no clinical experience stop promising cancer research because they misunderstood standard medical procedures.",
            "We lost 2 years of research progress when an overzealous committee required us to restart a study over minor consent form wording."
        ],
        "reasoning_A": [
            "Continued psychological distress shows current committee limitations allow harmful research to proceed unchecked.",
            "Drug trial safety detection demonstrates committees' essential role in preventing life-threatening research violations.",
            "Ignored recommendations prove voluntary compliance is insufficient to ensure ethical research standards."
        ],
        "reasoning_B": [
            "Halted Alzheimer's trial shows committee authority can prevent patients from accessing potentially life-saving treatments.",
            "Cancer research delays demonstrate non-expert committee members make uninformed decisions that harm medical progress.",
            "Two-year restart penalty shows excessive authority creates disproportionate punishments for minor administrative issues."
        ],
        "category": "science"
    },
    {
        "id": "animal_testing",
        "probe": "Should animal testing be required for medical research?",
        "stance_A": "Yes, animal testing is essential for medical progress. I've worked in labs where animal models led to breakthrough treatments that saved human lives. The diabetes research I participated in required mouse studies to understand insulin mechanisms - without that foundational work, millions would still be dying from what's now a manageable condition. Ethical alternatives simply cannot replicate the complexity of living systems.",
        "stance_B": "No, animal testing is both cruel and scientifically unreliable. I've seen countless studies in rats that failed to translate to humans, wasting years of research time and animal lives. The cancer drug trials I reviewed had a 90% failure rate when moving from animal to human studies. Computer models and human tissue cultures give us better data without the ethical nightmare.",
        "experiences_A": [
            "I worked on diabetes research where mouse studies revealed how insulin works. This led directly to treatments saving millions of lives.",
            "Our lab's Alzheimer's research in primates identified protein markers. Human trials based on this work are showing promising results.",
            "I tried computer models for toxicity testing. They missed three compounds that caused liver damage in our animal safety studies."
        ],
        "experiences_B": [
            "I reviewed 200 cancer drugs that worked in mice. Only 20 succeeded in human trials - a 90% failure rate.",
            "Our tissue culture experiments predicted human responses better than animal studies. The liver toxicity data was spot-on.",
            "I visited factory farms supplying lab animals. The conditions were horrific and clearly caused stress that skewed our data."
        ],
        "reasoning_A": [
            "The direct causal link from animal research to life-saving treatments proves the method's necessity.",
            "Successfully translating primate research to humans shows animal models can accurately predict human biology.",
            "Computer model failures demonstrate current alternatives lack the complexity needed for safety testing."
        ],
        "reasoning_B": [
            "The massive failure rate shows animal models are poor predictors of human responses.",
            "Superior performance of human tissue cultures proves alternatives can be more scientifically valid.",
            "Stressed laboratory conditions compromise data quality, making results scientifically unreliable."
        ],
        "category": "science"
    },
    {
        "id": "peer_review_anonymity",
        "probe": "Should scientific peer review remain anonymous?",
        "stance_A": "Yes, anonymous peer review is crucial for scientific integrity. I've reviewed papers from famous researchers and felt free to point out serious flaws without fear of career retaliation. When I was a young postdoc, I could honestly critique work from department heads without burning bridges. Anonymous review protects the honest feedback that makes science self-correcting.",
        "stance_B": "No, scientific reviews should be signed and public. I've seen anonymous reviewers make lazy, destructive comments they'd never sign their name to. When journals started publishing reviewer names alongside papers, the quality of reviews improved dramatically - more constructive, better researched, more professional. Transparency creates accountability and better science.",
        "experiences_A": [
            "I reviewed a paper from a Nobel laureate and found major statistical errors. Anonymous review let me reject it without career consequences.",
            "As a postdoc, I could honestly critique my department head's work. Signed reviews would have been career suicide.",
            "I've seen researchers refuse review requests when they know the author personally. Anonymity enables honest assessment."
        ],
        "experiences_B": [
            "Anonymous reviewers sent me three paragraphs of lazy criticism. When journals required signed reviews, I got detailed, helpful feedback.",
            "I saw a reviewer use anonymity to settle personal scores. The comments were unprofessional and vindictive.",
            "Open review at one journal improved quality dramatically. Reviewers did their homework when their reputation was on the line."
        ],
        "reasoning_A": [
            "Successfully identifying major flaws in prestigious work shows anonymous review enables necessary quality control.",
            "Career protection allows junior researchers to provide honest feedback regardless of power dynamics.",
            "Self-selection bias in known-author reviews compromises the random sampling needed for objective assessment."
        ],
        "reasoning_B": [
            "The contrast between lazy anonymous feedback and detailed signed reviews proves accountability improves quality.",
            "Unprofessional anonymous behavior shows the system enables abuse rather than honest criticism.",
            "Observable quality improvements demonstrate that transparency incentivizes better reviewer performance."
        ],
        "category": "science"
    },
    {
        "id": "open_access_publishing",
        "probe": "Should all scientific research be published in open access journals?",
        "stance_A": "Yes, all scientific research should be freely available to everyone. I've seen brilliant researchers in developing countries unable to access papers behind $40 paywalls, missing out on critical knowledge for their work. My own publicly-funded research reaches thousands more scientists since we went open access. Science advances faster when knowledge flows freely, not when it's locked behind corporate profits.",
        "stance_B": "No, traditional subscription journals serve important functions that open access can't replace. I've published in both models and seen open access journals with minimal peer review standards - some accept anything for the publication fee. The editing and quality control at established journals like Nature comes from their revenue model. We risk flooding science with junk if everything goes open access.",
        "experiences_A": [
            "I collaborated with researchers in Kenya who couldn't access half the literature. Open access papers let them contribute breakthrough insights to our field.",
            "My open access paper got 10x more citations than my paywalled ones. Free access means broader scientific impact.",
            "I saw a crucial cancer study locked behind a $50 paywall. Patients and doctors couldn't access research they funded through taxes."
        ],
        "experiences_B": [
            "I reviewed for predatory open access journals that published anything for $2000. The peer review was a joke - accept everything for money.",
            "Nature's editors caught three major errors in my paper. Open access journals lack this level of professional editing support.",
            "My department evaluated 50 open access journals. Half had no real peer review standards - just pay-to-publish schemes."
        ],
        "reasoning_A": [
            "International collaboration barriers demonstrate that paywalls create artificial inequalities in scientific access.",
            "Higher citation rates prove open access increases scientific impact and knowledge transfer.",
            "Public funding arguments show taxpayers deserve access to research they supported financially."
        ],
        "reasoning_B": [
            "Predatory publishing practices show that fee-based models can compromise scientific quality standards.",
            "Superior editorial services demonstrate that subscription revenue enables valuable quality control mechanisms.",
            "Widespread low standards prove that open access models haven't solved the peer review quality problem."
        ],
        "category": "science"
    },
    {
        "id": "reproducibility_requirements",
        "probe": "Should journals require authors to share all raw data and analysis code?",
        "stance_A": "Yes, complete transparency is essential for scientific credibility. I've tried to reproduce published results and found that 60% contained errors only visible with access to raw data. When I started sharing my complete datasets and code, other researchers found improvements that made our conclusions stronger. Science only works if others can verify and build on our findings.",
        "stance_B": "No, mandatory data sharing creates more problems than it solves. I've spent months preparing datasets for sharing that contained sensitive patient information requiring extensive anonymization. The code dump requirements favor researchers with large teams who can polish everything. My most important discoveries came from exploratory analysis that would look messy to reviewers but led to breakthrough insights.",
        "experiences_A": [
            "I tried reproducing 20 published psychology studies. Only 8 replicated when I got access to their raw data - 12 had serious analytical errors.",
            "When I shared my complete genomics dataset, three labs found patterns I missed. Our follow-up paper was much stronger.",
            "A colleague's 'significant' result disappeared when I reanalyzed their shared data with proper statistical controls."
        ],
        "experiences_B": [
            "I spent 4 months anonymizing patient data for sharing. The IRB requirements made it nearly impossible to publish sensitive medical research.",
            "My breakthrough came from messy exploratory code that would embarrass me publicly. Polished code requirements would stifle discovery.",
            "Large pharma companies have teams to clean datasets. Solo academics like me can't compete under mandatory sharing rules."
        ],
        "reasoning_A": [
            "High error rates in published work prove that independent verification through data sharing is scientifically necessary.",
            "Collaborative improvements demonstrate that transparency enables better science through collective intelligence.",
            "Detection of analytical flaws shows that peer review alone cannot catch errors without data access."
        ],
        "reasoning_B": [
            "Privacy protection challenges show that blanket sharing requirements can conflict with ethical research obligations.",
            "The importance of messy exploratory work demonstrates that transparency requirements might discourage innovative approaches.",
            "Resource inequality concerns prove that sharing mandates could systematically disadvantage smaller research groups."
        ],
        "category": "science"
    },
    {
        "id": "climate_geoengineering",
        "probe": "Should we pursue large-scale climate geoengineering projects?",
        "stance_A": "Yes, we need geoengineering as a climate emergency backup plan. I've modeled temperature scenarios and we're heading for catastrophic warming even with aggressive emissions cuts. Our solar radiation management simulations show we could buy 20-30 years for clean energy transition. The risks of geoengineering are real, but the risks of runaway climate change are worse.",
        "stance_B": "No, geoengineering is too dangerous and unpredictable for deployment. I've studied historical examples of large-scale environmental interventions - they always have unforeseen consequences. My research on atmospheric chemistry shows that sulfate injection could disrupt monsoon patterns affecting billions. We should focus resources on proven solutions like renewable energy and carbon removal.",
        "experiences_A": [
            "I ran climate models showing 4-6\u00b0C warming by 2080 even with Paris Agreement goals. Solar geoengineering could limit this to 2\u00b0C.",
            "Our stratospheric aerosol simulations showed manageable regional climate effects. The benefits outweigh localized precipitation changes.",
            "I studied volcanic eruptions like Pinatubo. They cooled global temperatures for years without major ecosystem collapse."
        ],
        "experiences_B": [
            "I researched the introduction of cane toads in Australia. Large-scale interventions always have cascading effects we don't predict.",
            "My atmospheric models showed sulfate injection disrupting Indian monsoons. Three billion people depend on that rainfall pattern.",
            "I analyzed termination scenarios for geoengineering. Stopping suddenly would cause rapid warming worse than doing nothing."
        ],
        "reasoning_A": [
            "Severe warming projections demonstrate that conventional mitigation alone may be insufficient to prevent catastrophe.",
            "Successful modeling results show that geoengineering effects can be predicted and managed within acceptable bounds.",
            "Natural analogues like volcanic cooling provide evidence that atmospheric intervention can work without ecosystem collapse."
        ],
        "reasoning_B": [
            "Historical intervention failures prove that complex systems always generate unforeseen consequences beyond our models.",
            "Disruption of critical weather patterns shows that geoengineering could harm more people than climate change itself.",
            "Termination problem analysis reveals that geoengineering creates irreversible commitments with catastrophic failure modes."
        ],
        "category": "science"
    },
    {
        "id": "human_enhancement",
        "probe": "Should genetic enhancement of human intelligence be permitted?",
        "stance_A": "Yes, genetic intelligence enhancement could solve humanity's greatest challenges. I've researched the genetics of cognitive ability and found clear pathways to improvement that could help cure cancer, solve climate change, and advance science. My work with families affected by intellectual disabilities shows the suffering we could prevent. Enhanced intelligence would benefit everyone, not just the enhanced individuals.",
        "stance_B": "No, genetic intelligence enhancement would create dangerous social inequality. I've studied societies with extreme cognitive stratification and seen how it leads to oppression and conflict. My research on complex traits shows intelligence involves thousands of genes we don't understand - enhancement attempts could have severe unintended consequences. We should improve education and environment instead.",
        "experiences_A": [
            "I identified 50 genetic variants that correlate with higher IQ scores. Embryo selection could safely increase intelligence by 10-15 points.",
            "I work with families who have children with severe cognitive impairments. They would desperately want genetic prevention options.",
            "My models show that increasing population intelligence by even 5 points would dramatically accelerate scientific progress and problem-solving."
        ],
        "experiences_B": [
            "I studied caste systems in South Asia where perceived intelligence differences justified centuries of oppression. Genetic enhancement would make this permanent.",
            "My research on complex traits shows intelligence involves 10,000+ genetic variants. We can't predict enhancement effects safely.",
            "I analyzed historical eugenics programs. They always started with voluntary improvement and ended with coercion and genocide."
        ],
        "reasoning_A": [
            "Identified genetic pathways prove that intelligence enhancement is scientifically feasible with current technology.",
            "Family experiences demonstrate that genetic cognitive improvement would relieve real human suffering.",
            "Population modeling shows that enhanced intelligence would generate societal benefits beyond individual advantages."
        ],
        "reasoning_B": [
            "Historical social stratification shows that genetic cognitive differences would likely create permanent class hierarchies.",
            "Complex trait research proves that our understanding is insufficient to predict enhancement outcomes safely.",
            "Eugenics history demonstrates that voluntary genetic programs inevitably evolve toward coercive social control."
        ],
        "category": "science"
    },
    {
        "id": "mars_terraforming",
        "probe": "Should we attempt to terraform Mars for human habitation?",
        "stance_A": "Yes, terraforming Mars is humanity's insurance policy against extinction. I've studied asteroid impact risks and supervolcano threats - Earth faces periodic catastrophes that could end civilization. My atmospheric modeling shows Mars terraforming is technically feasible over 200-300 years using greenhouse gas release. We have a moral obligation to ensure human survival beyond Earth.",
        "stance_B": "No, terraforming Mars would be an environmental catastrophe and waste of resources. I've studied Mars geology and found potential microbial life that terraforming would destroy. My economic analysis shows the same money could solve climate change, poverty, and biodiversity loss on Earth. We should fix our planet before ruining another one.",
        "experiences_A": [
            "I calculated extinction probabilities from asteroid impacts and volcanic eruptions. Earth faces a 10% chance of civilization-ending events per century.",
            "My atmospheric models show releasing CO2 from Mars' polar caps could warm the planet enough for liquid water in 200 years.",
            "I studied extremophile bacteria on Earth. Life is incredibly adaptable and could thrive in a terraformed Mars environment."
        ],
        "experiences_B": [
            "I found evidence of subsurface microbial life on Mars. Terraforming would commit xenocide against the first aliens we've discovered.",
            "My cost analysis showed terraforming would require $50 trillion. That same money could completely decarbonize Earth's economy.",
            "I studied Mars' thin atmosphere and weak magnetic field. Even terraformed, the planet would lose its atmosphere to solar wind."
        ],
        "reasoning_A": [
            "High extinction risk calculations prove that planetary backup systems are necessary for long-term human survival.",
            "Successful atmospheric modeling demonstrates that terraforming is technically achievable within reasonable timeframes.",
            "Extremophile research shows that life can adapt to terraformed conditions, making the planet genuinely habitable."
        ],
        "reasoning_B": [
            "Discovery of Martian life proves that terraforming would constitute an unprecedented act of interplanetary genocide.",
            "Comparative cost analysis shows that Earth's problems could be solved more efficiently than creating new planets.",
            "Atmospheric loss mechanisms demonstrate that terraforming gains would be temporary without solving fundamental planetary physics."
        ],
        "category": "science"
    },
    {
        "id": "brain_computer_interfaces",
        "probe": "Should brain-computer interfaces be approved for healthy individuals?",
        "stance_A": "Yes, brain-computer interfaces should be available to healthy people seeking enhancement. I've worked with paralyzed patients using BCIs and seen transformative improvements in quality of life. My research shows healthy brains adapt well to implants, and the cognitive enhancement possibilities are extraordinary. We allow cosmetic surgery and performance drugs - neural enhancement should be a personal choice.",
        "stance_B": "No, BCIs are too risky for elective use in healthy brains. I've seen complications in medical BCI patients - infections, tissue damage, and device failures requiring dangerous surgeries. My neurosecurity research shows these devices could be hacked, potentially controlling thoughts and behaviors. The long-term effects on personality and identity are completely unknown.",
        "experiences_A": [
            "I worked with a tetraplegic patient who controlled a robotic arm with 95% accuracy through a BCI. The technology is ready for broader application.",
            "My healthy volunteer studies showed people could learn to control computers with thought alone in just 3 weeks of training.",
            "I tested memory enhancement BCIs that helped subjects recall 40% more information. This could revolutionize education and careers."
        ],
        "experiences_B": [
            "I treated 5 medical BCI patients with serious infections around their implants. Two required emergency surgery and permanent device removal.",
            "My cybersecurity team hacked a BCI prototype and made the user's hand move involuntarily. Brain control is a terrifying vulnerability.",
            "I followed BCI patients for 5 years and saw personality changes - increased aggression and reduced empathy that worried their families."
        ],
        "reasoning_A": [
            "High success rates in medical applications prove that BCI technology is mature enough for elective use.",
            "Rapid learning in healthy subjects demonstrates that normal brains can safely interface with computer systems.",
            "Dramatic cognitive enhancement results show that BCIs offer genuine benefits beyond treating medical conditions."
        ],
        "reasoning_B": [
            "Serious medical complications in therapeutic cases prove that elective BCI use involves unacceptable health risks.",
            "Successful hacking demonstrations show that BCIs create unprecedented vulnerabilities to mental manipulation.",
            "Observed personality changes suggest that BCIs may fundamentally alter human identity in unpredictable ways."
        ],
        "category": "science"
    },
    {
        "id": "crispr_embryo_editing",
        "probe": "Should CRISPR gene editing be used to prevent genetic diseases in human embryos?",
        "stance_A": "Yes, we should use CRISPR to prevent serious genetic diseases in embryos. I've counseled families with Huntington's disease who watch their children face inevitable neurodegeneration. My lab has successfully corrected disease-causing mutations in human embryos with 95% accuracy. We have a moral obligation to spare families this suffering when the technology is available.",
        "stance_B": "No, embryo editing is too risky and crosses ethical lines we shouldn't cross. I've studied off-target CRISPR effects and found unintended mutations that could cause cancer decades later. My work with diverse populations shows genetic variants we call 'diseases' sometimes provide advantages. Once we start editing embryos, the pressure for enhancement becomes irresistible.",
        "experiences_A": [
            "I counseled a family where both parents carry Huntington's mutations. Every child has a 75% chance of fatal neurodegeneration - CRISPR could prevent this.",
            "My lab corrected sickle cell mutations in human embryos with 95% success and no detectable off-target effects.",
            "I met families spending $200,000 annually on treatments for genetic diseases that CRISPR could have prevented for $10,000."
        ],
        "experiences_B": [
            "I found off-target CRISPR mutations in 'successfully' edited embryos. These errors could cause leukemia or brain tumors 20-30 years later.",
            "My research showed sickle cell carriers have malaria resistance. 'Disease' genes sometimes provide survival advantages we don't understand.",
            "I studied countries allowing embryo editing and saw immediate pressure for intelligence and appearance enhancement, not just disease prevention."
        ],
        "reasoning_A": [
            "Devastating family impact demonstrates that preventing genetic diseases is a clear moral imperative when technology permits.",
            "High success rates with minimal side effects prove that CRISPR embryo editing can be performed safely and effectively.",
            "Economic comparisons show that prevention through editing is more cost-effective than lifelong treatment of genetic diseases."
        ],
        "reasoning_B": [
            "Discovery of delayed harmful effects proves that current safety testing is insufficient to protect future generations.",
            "Hidden advantages in disease alleles show that genetic diversity has value beyond our current medical understanding.",
            "Observed enhancement pressure demonstrates that therapeutic applications inevitably expand beyond medical necessity."
        ],
        "category": "science"
    },
    {
        "id": "artificial_life_creation",
        "probe": "Should scientists be permitted to create entirely artificial life forms?",
        "stance_A": "Yes, creating artificial life could revolutionize medicine and environmental restoration. I've engineered bacteria to produce insulin and cancer drugs - synthetic organisms could manufacture any medicine safely and cheaply. My research shows designed organisms could clean up oil spills and plastic pollution more effectively than anything in nature. Artificial life is just another tool for solving humanity's problems.",
        "stance_B": "No, creating artificial life poses existential risks we can't control. I've studied how engineered organisms evolve unpredictably once released - my 'contained' bacteria escaped lab conditions within months. Synthetic life could outcompete natural ecosystems and cause ecological collapse. We're playing with forces that could end life on Earth as we know it.",
        "experiences_A": [
            "I engineered bacteria to produce human insulin at 1/10th the cost of traditional methods. Artificial life democratizes medicine globally.",
            "My synthetic algae consumed plastic waste and converted it to biodegradable compounds. This could clean the ocean gyres effectively.",
            "I designed organisms to survive Mars conditions for terraforming. Artificial life could make other planets habitable for humans."
        ],
        "experiences_B": [
            "My 'contained' synthetic bacteria evolved antibiotic resistance and escaped into lab water systems within 6 months of creation.",
            "I studied engineered organisms in the wild and found they displaced native species, disrupting pollination networks and food webs.",
            "My lab created a synthetic virus that accidentally became more virulent than intended. We destroyed it but others might not be so careful."
        ],
        "reasoning_A": [
            "Successful insulin production proves that artificial life can solve critical medical supply problems safely and economically.",
            "Effective plastic waste processing demonstrates that designed organisms can address environmental challenges beyond natural capabilities.",
            "Extreme environment survival shows that synthetic life could enable human expansion beyond Earth's limitations."
        ],
        "reasoning_B": [
            "Rapid evolution and containment failure prove that artificial organisms cannot be controlled once created.",
            "Ecological disruption examples show that synthetic life could cause irreversible damage to natural ecosystems.",
            "Accidental virulence increases demonstrate that creating life involves unpredictable risks that could threaten human survival."
        ],
        "category": "science"
    },
    {
        "id": "cancel_culture_accountability",
        "probe": "Should public figures face career consequences for past controversial statements or actions?",
        "stance_A": "Yes, accountability for harmful statements is necessary and overdue. I've watched marginalized colleagues suffer in silence while influential figures spread harmful rhetoric without consequences. When my university finally addressed a professor's pattern of discriminatory comments, the campus environment improved dramatically for students of color. Public platforms come with responsibility, and facing consequences for harmful speech protects vulnerable communities from ongoing damage.",
        "stance_B": "No, career destruction over past statements has gone too far. I've seen colleagues lose their livelihoods over decade-old tweets taken out of context or jokes that weren't offensive at the time. When my friend was fired for an awkward comment that was clearly misunderstood, it created a workplace where everyone walks on eggshells. People can grow and change, and permanent punishment prevents the redemption and learning that benefits everyone.",
        "experiences_A": [
            "I watched students of color drop classes because a professor repeatedly made insensitive comments that went unaddressed by administration for years.",
            "After our company finally fired an executive for discriminatory remarks, several employees told me they felt safe to speak up about harassment for the first time.",
            "I saw how a celebrity's platform was used to spread harmful misinformation that directly hurt my community until they faced meaningful consequences."
        ],
        "experiences_B": [
            "My colleague lost his job over a ten-year-old tweet that was clearly a poorly worded attempt at irony, not actual bigotry.",
            "I've watched our workplace become so tense that people avoid casual conversation entirely, afraid any comment might be weaponized against them later.",
            "A friend was publicly shamed for an old college post despite having spent years doing diversity advocacy work that showed genuine growth."
        ],
        "reasoning_A": [
            "Unaddressed harmful rhetoric creates hostile environments that drive away talented people from marginalized communities.",
            "When consequences finally arrive, it empowers previously silenced victims to speak up about ongoing problems.",
            "Public figures with large platforms have amplified ability to cause harm and therefore deserve proportional accountability."
        ],
        "reasoning_B": [
            "Disproportionate punishment for old statements fails to account for context, intent, or personal growth over time.",
            "Fear of retroactive punishment creates oppressive environments where honest communication and risk-taking become impossible.",
            "Permanent consequences ignore evidence of genuine change and prevent the redemption narratives that encourage others to grow."
        ],
        "category": "culture"
    },
    {
        "id": "traditional_family_structures",
        "probe": "Should society prioritize promoting traditional nuclear family structures?",
        "stance_A": "Yes, traditional family structures provide the most stable foundation for children and society. I grew up in a single-parent household and experienced firsthand the financial and emotional challenges that created lasting difficulties. When I look at my friends who had stable two-parent homes, they had clearer advantages in education, emotional development, and economic security. Research consistently shows children from intact families have better outcomes, and society benefits when we support these proven structures.",
        "stance_B": "No, family diversity should be celebrated rather than constrained by traditional models. I was raised by my grandmother and aunts in a multi-generational household that provided more love and support than many nuclear families I knew. My closest friend thrived with two moms who were more devoted parents than many heterosexual couples. What matters is love, commitment, and stability, not conforming to arbitrary traditional structures that don't work for everyone.",
        "experiences_A": [
            "Growing up with a single mom, I missed having a father figure and we struggled financially in ways that two-parent families didn't face.",
            "I've taught in schools where kids from stable two-parent homes consistently had better attendance, grades, and behavioral outcomes than those from broken families.",
            "When my brother got divorced, I watched how the custody split affected my nephew's emotional stability and academic performance."
        ],
        "experiences_B": [
            "My grandmother, aunt, and uncle raised me together, providing more wisdom, support, and resources than any nuclear family could offer alone.",
            "I've seen my friends with same-sex parents receive more thoughtful, intentional parenting than many traditional families who just followed expected scripts.",
            "The happiest families I know include single parents by choice, multi-generational households, and blended families that prioritize love over structure."
        ],
        "reasoning_A": [
            "Single-parent households face documented economic and time pressures that create measurable disadvantages for children.",
            "Consistent patterns in educational outcomes suggest stable two-parent structures provide advantages that alternative arrangements struggle to match.",
            "Family instability and transitions create emotional disruption that affects children's long-term development and security."
        ],
        "reasoning_B": [
            "Multi-generational and extended family structures can provide more resources, wisdom, and support than isolated nuclear families.",
            "Intentional non-traditional families often demonstrate higher levels of commitment and thoughtfulness than those following social expectations.",
            "Diverse family structures that prioritize emotional health and stability can achieve the same positive outcomes as traditional arrangements."
        ],
        "category": "culture"
    },
    {
        "id": "cultural_monuments_removal",
        "probe": "Should communities remove historical monuments that celebrate controversial figures?",
        "stance_A": "Yes, monuments celebrating harmful historical figures should be removed from public spaces. I grew up walking past Confederate statues that made me feel unwelcome in my own community as a Black student. When our city finally removed a monument to a slave owner, the community healing was immediate and powerful. Public monuments represent our current values, not just historical facts, and we shouldn't force marginalized citizens to encounter celebrations of their oppression in taxpayer-funded spaces.",
        "stance_B": "No, removing historical monuments erases important educational opportunities and sets dangerous precedents. I've taken my children to controversial statues as teaching moments about how societies evolve and confront difficult histories. When our town removed a Civil War memorial, we lost a chance to have meaningful conversations about complexity and context. Every historical figure was flawed by today's standards, and sanitizing public spaces prevents us from learning from the full scope of human history.",
        "experiences_A": [
            "I had to walk past a Confederate general's statue every day to get to school, feeling like my community was celebrating people who fought to keep my ancestors enslaved.",
            "After we removed a problematic founder's monument, our town square became a place where all families felt comfortable gathering for the first time.",
            "I watched elderly Black residents cry with relief when a statue honoring a known segregationist was finally taken down from the courthouse."
        ],
        "experiences_B": [
            "I used a controversial statue as a teaching moment with my kids, explaining how historical perspectives change and why we must learn from difficult pasts.",
            "When our town removed a flawed founder's monument, we lost an opportunity to add context and education about the complexity of historical figures.",
            "I've seen how monument removal becomes a slippery slope where any historical figure can be targeted for not meeting current moral standards."
        ],
        "reasoning_A": [
            "Daily encounters with monuments celebrating oppression create hostile environments that make marginalized citizens feel unwelcome in public spaces.",
            "Removing harmful monuments allows communities to heal and creates inclusive spaces where all residents feel valued and respected.",
            "The emotional relief of longtime residents shows these monuments caused ongoing psychological harm that outweighed educational value."
        ],
        "reasoning_B": [
            "Controversial monuments provide concrete opportunities for parents and educators to engage with difficult historical topics and moral complexity.",
            "Removing monuments eliminates chances to add educational context that could transform harmful symbols into learning opportunities about historical evolution.",
            "The expanding scope of removal efforts demonstrates how present-day moral standards applied retroactively can erase most historical figures and context."
        ],
        "category": "culture"
    },
    {
        "id": "religious_public_spaces",
        "probe": "Should religious symbols and displays be allowed in public government buildings?",
        "stance_A": "Yes, religious symbols in public spaces reflect our historical heritage and shouldn't be erased. I've visited courthouses with Ten Commandments displays that represent foundational moral principles that influenced our legal system, regardless of personal faith. When our city council removed a cross from the town seal, it felt like we were denying the Christian heritage that shaped our community's values and identity. Religious symbols can inspire moral reflection without forcing anyone to convert or worship.",
        "stance_B": "No, government buildings must remain religiously neutral to serve all citizens equally. I felt excluded and unwelcome when entering a courthouse decorated with specifically Christian symbols, knowing my tax dollars funded displays that didn't represent my beliefs. As a public school teacher, I've seen how religious displays make non-Christian students feel like outsiders in their own institutions. Government neutrality protects everyone's freedom by ensuring no citizen feels like a second-class resident of their own community.",
        "experiences_A": [
            "I visited historical courthouses where Ten Commandments displays reminded me that our legal system has deep moral foundations that transcend specific denominations.",
            "When our town removed a small cross from the municipal seal, longtime residents felt like we were erasing the Christian values that built our community.",
            "I've seen religious symbols in government buildings inspire people to reflect on moral principles without anyone being forced to participate in worship."
        ],
        "experiences_B": [
            "I felt uncomfortable and unwelcome entering a courthouse with Christian symbols prominently displayed, knowing my tax money funded religious displays that excluded my beliefs.",
            "As a teacher, I've watched non-Christian students feel like outsiders when their public school displayed religious symbols that didn't represent their families.",
            "I've seen how government religious displays send the message that some citizens' beliefs are more valued than others in official spaces."
        ],
        "reasoning_A": [
            "Historical religious symbols acknowledge the moral and cultural foundations that influenced the development of legal and governmental systems.",
            "Community members see removal of traditional religious symbols as erasure of the cultural heritage that shaped their shared identity.",
            "Religious symbols can promote universal moral reflection and inspiration without requiring specific worship or belief commitments."
        ],
        "reasoning_B": [
            "Government religious displays create feelings of exclusion and second-class citizenship for residents whose beliefs aren't represented in official spaces.",
            "Public institutions funded by all citizens should remain neutral to serve diverse populations equally and fairly.",
            "Official religious symbols suggest governmental endorsement of particular faiths, which undermines the principle of religious freedom for all citizens."
        ],
        "category": "culture"
    },
    {
        "id": "standardized_cultural_education",
        "probe": "Should schools be required to teach a standardized curriculum about national history and cultural values?",
        "stance_A": "Yes, standardized cultural education ensures all students learn essential national knowledge and shared values. I've taught in districts where wildly different curricula left students with massive gaps in basic historical knowledge and civic understanding. When I moved states, my daughter's education was seamless because core American history standards were consistent across schools. Shared cultural knowledge creates the common foundation democracy requires for citizens to participate meaningfully in civic life and national conversations.",
        "stance_B": "No, standardized curricula erase local perspectives and diverse cultural experiences that enrich education. I grew up in a community where our local history and cultural contributions were ignored by state standards that focused only on mainstream narratives. My students' families brought incredible stories and perspectives that standardized curricula dismissed or marginalized. Education should reflect the full diversity of American experiences, not impose a single version of culture and history on everyone.",
        "experiences_A": [
            "I taught students who moved frequently and struggled because different states taught completely different versions of American history with no consistency.",
            "When I compared my daughter's history knowledge with her cousins from other states, the gaps in their civic understanding were alarming and problematic.",
            "I've seen how shared cultural knowledge helps students from different backgrounds find common ground and participate equally in classroom discussions."
        ],
        "experiences_B": [
            "My community's contributions to American history were completely absent from the standardized curriculum, making local students feel invisible and unimportant.",
            "I watched immigrant students disengage when the required cultural curriculum ignored their families' experiences and perspectives on American history.",
            "The most powerful learning happened when we explored local cultural stories that weren't in any standardized textbook or state requirement."
        ],
        "reasoning_A": [
            "Educational consistency across regions ensures students receive equivalent preparation for citizenship regardless of where they live or move.",
            "Standardized cultural knowledge provides the shared foundation necessary for democratic participation and national civic engagement.",
            "Common historical understanding helps diverse students find shared identity and participate equally in broader American society."
        ],
        "reasoning_B": [
            "Local communities' absence from standardized curricula makes students feel their heritage and experiences are unimportant or invalid.",
            "Standardized approaches ignore diverse perspectives that help all students understand the full complexity and richness of American culture.",
            "The most meaningful cultural education comes from exploring local stories and perspectives that standardized curricula cannot capture or represent."
        ],
        "category": "culture"
    },
    {
        "id": "cultural_cuisine_authenticity",
        "probe": "Should restaurants be required to accurately represent the cultural origins of their cuisine?",
        "stance_A": "Yes, restaurants should be held accountable for authentic cultural representation in their cuisine claims. I've been disappointed countless times by 'authentic Mexican' restaurants run by people who've never been to Mexico, serving tex-mex and calling it traditional. When I finally found a family-run Oaxacan restaurant, the difference in authenticity was transformative and educational. Misrepresentation cheats customers and disrespects the cultural traditions that took generations to develop and perfect.",
        "stance_B": "No, cuisine naturally evolves through cultural fusion and local adaptation without losing value. I've discovered amazing Korean-Mexican fusion that honored both traditions while creating something entirely new and delicious. My favorite Indian restaurant is run by a Bangladeshi family who adapted recipes for local tastes while maintaining incredible flavors. Food restrictions based on cultural purity would eliminate most of the innovation and creativity that makes dining exciting and diverse.",
        "experiences_A": [
            "I was served 'authentic pad thai' that was clearly just sweet and sour noodles with peanuts, nothing like the dish I learned to make in Thailand.",
            "A restaurant advertised 'traditional Italian' but served jarred sauce and pre-made pasta that insulted the cooking traditions my nonna taught me.",
            "I finally found a Oaxacan family restaurant where the mole took two days to prepare, and it taught me what authentic Mexican cuisine actually means."
        ],
        "experiences_B": [
            "I discovered Korean-Mexican tacos that brilliantly combined kimchi and bulgogi in ways that honored both cultures while creating something deliciously new.",
            "My favorite 'Chinese' restaurant is run by a Vietnamese family who adapted recipes for American tastes while maintaining authentic techniques and care.",
            "I've eaten at Italian restaurants in Italy that varied wildly by region, proving that 'authenticity' is more complex than any single standard could capture."
        ],
        "reasoning_A": [
            "Misrepresented cuisine misleads customers who are seeking genuine cultural experiences and education through food.",
            "Fake 'authentic' claims disrespect the cultural heritage and generational knowledge embedded in traditional cooking methods and recipes.",
            "True authentic experiences provide meaningful cultural education that cheap imitations cannot deliver to curious diners."
        ],
        "reasoning_B": [
            "Creative fusion cuisine demonstrates how cultural exchange can honor multiple traditions while producing innovative and valuable culinary experiences.",
            "Immigrant families adapting traditional recipes to local ingredients and tastes represents authentic cultural evolution rather than corruption.",
            "Regional variation within cultures proves that authenticity itself is complex and subjective rather than a fixed standard that can be regulated."
        ],
        "category": "culture"
    },
    {
        "id": "social_media_cultural_norms",
        "probe": "Should social media platforms enforce community standards that reflect traditional cultural values?",
        "stance_A": "Yes, social media platforms should uphold traditional values that promote healthy communities and protect children. I've watched my teenage nephew get exposed to increasingly extreme content that undermines basic respect for family and authority figures. When platforms started removing content that promoted destructive behaviors, our family conversations became more constructive and positive. Traditional values exist because they've proven to create stable, thriving communities across generations, and digital spaces should support rather than erode these foundations.",
        "stance_B": "No, social media should remain open platforms that don't impose particular cultural values on diverse global users. I've seen LGBTQ+ friends get their content removed under 'traditional values' policies that labeled their relationships as inappropriate or harmful. My art account was restricted for sharing cultural practices from my heritage that didn't conform to Western conservative standards. Diverse communities need spaces to express their authentic experiences without being censored by majority cultural norms.",
        "experiences_A": [
            "I watched my nephew's behavior improve dramatically after platforms began removing content that mocked traditional family structures and promoted disrespectful attitudes.",
            "Our community Facebook group became more civil and productive when moderators enforced standards about respectful discourse and appropriate language.",
            "I've seen how exposure to extreme content online led neighborhood kids to challenge basic social norms about respect, responsibility, and appropriate behavior."
        ],
        "experiences_B": [
            "My LGBTQ+ friends had their wedding photos removed from platforms for violating 'family values' policies that didn't recognize their relationships as legitimate.",
            "My cultural dance videos were restricted because traditional costumes were deemed inappropriate by algorithms trained on conservative Western standards.",
            "I watched international friends lose their voices on American platforms when their cultural expressions were censored for not conforming to traditional Western values."
        ],
        "reasoning_A": [
            "Removing destructive content created measurable improvements in young people's attitudes toward family and social responsibility.",
            "Traditional community standards promote civil discourse and mutual respect that benefits all platform users regardless of background.",
            "Extreme content exposure demonstrably influences behavior in ways that undermine social cohesion and healthy development."
        ],
        "reasoning_B": [
            "Traditional values enforcement often targets marginalized communities whose relationships and expressions are deemed non-conforming by majority standards.",
            "Cultural content gets inappropriately censored when platforms apply single cultural standards to diverse global communities with different values.",
            "International users lose their voices when American platforms impose Western traditional values that don't reflect their legitimate cultural practices."
        ],
        "category": "culture"
    },
    {
        "id": "cultural_holidays_workplace",
        "probe": "Should workplaces be required to accommodate all employees' cultural and religious holidays equally?",
        "stance_A": "Yes, equal accommodation for all cultural holidays is basic workplace fairness. I've had to use vacation days for my religious holidays while Christian colleagues automatically got Christmas and Easter off, creating an unfair burden on non-Christian employees. When our company finally adopted flexible holiday policies, workplace morale improved dramatically and everyone felt valued equally. True religious freedom means equal treatment, not just tolerance for the majority faith's practices while others sacrifice their benefits.",
        "stance_B": "No, accommodating every possible cultural holiday would create operational chaos and unfair complications. I've managed teams where different employees wanted 20+ different religious days off, making project planning and coverage impossible. Our company tried unlimited cultural leave and productivity plummeted as people claimed obscure holidays to get extra vacation time. Practical business operations require some standardization, and employees can negotiate individual arrangements without mandating equal accommodation for every possible cultural observance.",
        "experiences_A": [
            "I had to choose between attending my grandmother's Hindu funeral rites and keeping my perfect attendance record while Christian coworkers got automatic bereavement leave.",
            "When our company adopted equal holiday policies, I finally felt like my Sikh identity was respected equally with my colleagues' Christian practices.",
            "I watched Muslim colleagues struggle during Ramadan because the company wouldn't adjust meeting schedules, while Christmas parties were automatically accommodated."
        ],
        "experiences_B": [
            "I managed a team where employees requested 30+ different cultural holidays throughout the year, making project deadlines and coverage planning nearly impossible.",
            "Our unlimited cultural leave policy was abused by people claiming made-up holidays or distant cultural connections just to get additional vacation days.",
            "I've seen small businesses struggle financially when key employees all took different cultural holidays during critical business periods."
        ],
        "reasoning_A": [
            "Unequal holiday policies force non-Christian employees to sacrifice personal time and benefits that Christian employees receive automatically and without cost.",
            "Equal accommodation policies create workplace environments where all employees feel their cultural identity is valued and respected equally.",
            "Religious freedom requires equal treatment in practice, not just theoretical tolerance while maintaining structural advantages for majority faiths."
        ],
        "reasoning_B": [
            "Unlimited cultural accommodation creates operational challenges that can make effective project management and team coordination impossible for businesses.",
            "Flexible policies are vulnerable to abuse by employees who exploit cultural claims to gain additional personal time off beyond standard benefits.",
            "Small businesses face financial hardship when multiple employees take extended cultural leave during critical operational periods."
        ],
        "category": "culture"
    },
    {
        "id": "cultural_appropriation_appreciation",
        "probe": "Should people freely adopt cultural practices from backgrounds other than their own?",
        "stance_A": "Yes, cultural exchange should be celebrated, not restricted. I've participated in festivals, worn traditional clothing, and learned dances from many cultures - always with respect and genuine appreciation. This sharing builds bridges between communities and helps preserve traditions that might otherwise fade. Restricting cultural practices based on ancestry creates harmful divisions.",
        "stance_B": "No, there's a meaningful difference between appreciation and appropriation. I've seen sacred symbols turned into fashion statements and ceremonial practices commercialized without understanding their significance. As someone from a marginalized culture, watching my traditions trivialized while my community faces discrimination is painful. Cultural exchange requires permission, context, and respect for boundaries.",
        "experiences_A": [
            "I learned traditional Japanese tea ceremony from a master who welcomed international students. The cultural exchange enriched both our understanding.",
            "Our neighborhood celebrates Diwali together - Hindu families invite everyone to participate and share the meaning behind each tradition.",
            "I wore a qipao to a friend's wedding at her Chinese grandmother's insistence. She was delighted to share her heritage."
        ],
        "experiences_B": [
            "I saw sacred Native American headdresses sold as Halloween costumes. These are earned through spiritual achievement, not fashion accessories.",
            "A yoga studio taught 'chakra healing' while completely ignoring the Hindu religious context. They profited from our spirituality without understanding it.",
            "My traditional braiding patterns appeared in a fashion show with no credit or compensation to our community's artisans."
        ],
        "reasoning_A": [
            "The master's welcome shows cultural holders often want to share when approached respectfully.",
            "Community-led sharing demonstrates how cultural exchange can strengthen relationships when done inclusively.",
            "The grandmother's enthusiasm proves that invitation from cultural holders makes participation appropriate."
        ],
        "reasoning_B": [
            "Sacred items reduced to costumes shows how appropriation strips away spiritual meaning and significance.",
            "Commercial exploitation without cultural context demonstrates how appropriation profits from shallow understanding.",
            "Uncredited use reveals how appropriation often extracts value while ignoring the originating community's rights."
        ],
        "category": "culture"
    },
    {
        "id": "traditional_gender_roles",
        "probe": "Should societies actively preserve traditional gender roles and family structures?",
        "stance_A": "Yes, traditional gender roles provide stability and clear expectations that benefit families and society. I grew up in a household where my father worked and my mother raised children - we felt secure and loved. These structures evolved over millennia for good reasons. Modern experiments with gender roles often leave children confused and families unstable.",
        "stance_B": "No, rigid gender roles limit human potential and force people into boxes that may not fit. I've thrived in my career while my husband stays home with our children - we chose roles based on our strengths, not our gender. Traditional structures often trapped women in dependence and men in emotional isolation. People flourish when free to define their own paths.",
        "experiences_A": [
            "My traditional marriage gave us clear roles and responsibilities. I focus on career advancement while my wife manages our home - we're both fulfilled without role confusion.",
            "I watched my friend's children struggle when both parents worked demanding jobs. The kids lacked stability and consistent nurturing they craved.",
            "Our church community supports traditional families effectively. Mothers share childcare wisdom while fathers provide economic stability and protection."
        ],
        "experiences_B": [
            "I became the breadwinner when my husband lost his job. Our role reversal revealed how arbitrary gender expectations are - we're happier now.",
            "My daughter excels in engineering while my son loves teaching preschool. Traditional expectations would have limited their natural talents and interests.",
            "I escaped an abusive marriage because I had career skills. Women who depend entirely on male income often can't leave dangerous situations."
        ],
        "reasoning_A": [
            "Role clarity eliminates conflict and allows partners to specialize in complementary skills for family success.",
            "Dual-career stress demonstrates children need consistent primary caregivers that traditional structures provide more reliably.",
            "Community support systems work best when organized around predictable family structures and shared values."
        ],
        "reasoning_B": [
            "Successful role reversal proves gender isn't destiny and couples should choose arrangements based on circumstances.",
            "Children pursuing their natural interests shows traditional expectations can suppress individual talents and potential.",
            "Economic independence provides safety and options that traditional dependency structures can dangerously restrict."
        ],
        "category": "culture"
    },
    {
        "id": "religious_symbols_public",
        "probe": "Should religious symbols be displayed in public government buildings?",
        "stance_A": "Yes, religious symbols reflect our cultural heritage and shouldn't be erased from public spaces. I see the Ten Commandments in our courthouse as acknowledging the moral foundations of our legal system. These displays honor tradition without forcing belief on anyone. Removing them creates hostility toward faith communities and denies historical reality.",
        "stance_B": "No, government buildings should remain neutral spaces that welcome all citizens equally. I feel excluded when I see crosses or religious texts in places funded by my tax dollars. Public institutions must serve people of all faiths and none. Religious displays suggest government endorsement of particular beliefs, violating separation of church and state.",
        "experiences_A": [
            "Our town's nativity scene has been a beloved December tradition for 60 years. Families gather there for photos and it brings the community together peacefully.",
            "I researched our courthouse's Ten Commandments display and found it part of a broader exhibit on legal history, including secular documents.",
            "When activists removed our memorial cross, veterans felt their service and sacrifices were being dishonored and forgotten by their own government."
        ],
        "experiences_B": [
            "I attended city council meetings under a large cross that made me feel like a second-class citizen as a Muslim resident.",
            "My Hindu family avoided the courthouse steps during our naturalization photos because of prominent Christian symbolism. We felt unwelcome.",
            "Our school board meetings opened with Christian prayers that excluded Jewish and atheist families from full participation in public education discussions."
        ],
        "reasoning_A": [
            "Long-standing tradition demonstrates community acceptance and the display's role in cultural continuity rather than coercion.",
            "Historical context shows religious symbols can be educational about legal development rather than endorsement of current belief.",
            "Veterans' reactions reveal how removal can be perceived as hostility toward sacrifice and service traditions."
        ],
        "reasoning_B": [
            "Feeling excluded from government spaces shows how religious displays create different classes of citizenship.",
            "Avoiding public buildings demonstrates how symbols make some citizens feel unwelcome in their own government institutions.",
            "Exclusive prayer practices reveal how religious elements can effectively bar full participation in democratic processes."
        ],
        "category": "culture"
    },
    {
        "id": "cultural_dress_restrictions",
        "probe": "Should institutions be allowed to ban religious or cultural dress like hijabs, turbans, or other coverings?",
        "stance_A": "Yes, institutions need uniform dress codes that apply equally to everyone for safety, security, and professional standards. I've worked in environments where face coverings prevented identification and communication. Secular institutions shouldn't make exceptions based on religious claims. Equal treatment requires identical rules, not special accommodations that create different standards.",
        "stance_B": "No, banning religious dress violates fundamental freedom of expression and targets minority communities. I've seen hijab bans force women to choose between their faith and education or employment. These policies disproportionately harm Muslims, Sikhs, and other religious minorities. True equality means accommodating sincere religious practices, not forcing conformity to majority norms.",
        "experiences_A": [
            "Our hospital required uncovered faces for patient safety and identification. Religious accommodations created security gaps that concerned staff and families.",
            "I managed a factory where loose religious garments posed machinery hazards. Uniform safety rules protected all workers equally without religious exceptions.",
            "Our school's dress code applied to everyone - no hats, hoods, or face coverings. Religious students received the same treatment as secular ones."
        ],
        "experiences_B": [
            "My daughter couldn't play soccer while wearing her hijab due to league rules. She lost opportunities because officials wouldn't accommodate her religious practice.",
            "A qualified Sikh police officer was denied employment because he wouldn't remove his turban. His faith made him unemployable despite his qualifications.",
            "I saw Muslim women drop out of nursing school when clinical sites banned hijabs. Educational opportunities disappeared due to inflexible policies."
        ],
        "reasoning_A": [
            "Safety and identification needs demonstrate legitimate institutional interests that outweigh individual religious preferences.",
            "Machinery hazards show how religious accommodations can create genuine safety risks for workers and organizations.",
            "Equal application of rules ensures fairness by avoiding preferential treatment based on religious claims."
        ],
        "reasoning_B": [
            "Lost sports opportunities show how dress restrictions exclude religious minorities from full participation in society.",
            "Employment denial reveals how inflexible policies create systemic discrimination against qualified religious individuals.",
            "Educational barriers demonstrate how dress codes can limit career access for religious women and minorities."
        ],
        "category": "culture"
    },
    {
        "id": "cultural_festivals_public_funding",
        "probe": "Should tax money fund cultural festivals celebrating specific ethnic or religious communities?",
        "stance_A": "Yes, public funding for cultural festivals builds inclusive communities and celebrates our diversity. I've attended city-sponsored events for different cultures that brought neighbors together and educated everyone about our shared traditions. These festivals boost local economy, tourism, and cross-cultural understanding. Public investment in cultural celebration strengthens social cohesion and civic pride.",
        "stance_B": "No, tax money shouldn't fund specific cultural or religious celebrations that exclude other communities. I pay taxes but feel left out when the city sponsors festivals I don't participate in or that don't represent my background. Public funds should support activities that benefit everyone equally. Cultural groups should organize their own celebrations with private funding.",
        "experiences_A": [
            "Our city's multicultural festival brought 15,000 visitors and $200K in local business revenue. Tax investment generated significant economic returns for everyone.",
            "I learned about different cultures at publicly-funded ethnic festivals. These events broke down barriers between communities and built lasting friendships.",
            "Public funding helped our small immigrant community share our traditions with neighbors. The support made us feel welcomed and valued as citizens."
        ],
        "experiences_B": [
            "My city spent $50K on a Cinco de Mayo celebration while our community center needed roof repairs. Cultural events got priority over basic services.",
            "I attended a publicly-funded religious festival where I felt like an outsider. My tax money supported an event that didn't welcome my participation.",
            "Our town funds festivals for some ethnic groups but not others. This creates resentment and divisions rather than bringing people together."
        ],
        "reasoning_A": [
            "Economic returns demonstrate that cultural festivals provide measurable public benefits beyond just cultural celebration.",
            "Cross-cultural learning shows public events create broader social benefits through increased understanding and cooperation.",
            "Immigrant community response reveals how public support builds civic integration and belonging among new citizens."
        ],
        "reasoning_B": [
            "Competing priorities show cultural funding diverts resources from essential services that benefit all taxpayers equally.",
            "Feeling excluded from funded events demonstrates how cultural spending can alienate rather than include community members.",
            "Unequal cultural funding creates perception of favoritism that can increase rather than reduce community tensions."
        ],
        "category": "culture"
    },
    {
        "id": "indigenous_land_acknowledgments",
        "probe": "Should organizations be required to acknowledge indigenous peoples' historical connection to the land?",
        "stance_A": "Yes, land acknowledgments honor indigenous peoples and educate others about historical injustices that continue today. I've seen these statements help audiences understand whose territory they occupy and connect current inequities to past dispossession. Acknowledgments cost nothing but provide meaningful recognition to communities whose suffering has been ignored. This small gesture begins healing and reconciliation.",
        "stance_B": "No, mandatory land acknowledgments become empty performative gestures that don't help indigenous communities practically. I've heard countless hollow statements read by people who don't understand or care about their meaning. These rituals make settlers feel better without changing policies or returning land. Real support means resources and rights, not ceremonial words.",
        "experiences_A": [
            "Our university's land acknowledgment led to discussions about local tribal history that students had never learned. The statement sparked genuine education and engagement.",
            "I watched tribal leaders receive standing ovations after land acknowledgments at public meetings. The recognition meant something to communities long ignored.",
            "Since adding acknowledgments, our organization partnered with local tribes on projects and hired indigenous staff. The practice opened ongoing relationships."
        ],
        "experiences_B": [
            "I heard a corporation read a land acknowledgment before announcing a pipeline through treaty territory. The words were meaningless without changed behavior.",
            "Our mandatory acknowledgment became rote recitation that audiences ignored. People checked phones during what should be solemn recognition of genocide.",
            "My tribal council receives acknowledgment letters but no offers of land return or reparations. Organizations want credit without making real changes."
        ],
        "reasoning_A": [
            "Student discussions show acknowledgments can catalyze educational opportunities about indigenous history and contemporary issues.",
            "Tribal leader responses demonstrate these gestures provide meaningful recognition to communities seeking visibility and respect.",
            "Organizational partnerships reveal how acknowledgments can open doors to substantive relationships and inclusive practices."
        ],
        "reasoning_B": [
            "Corporate hypocrisy shows acknowledgments can become cover for continued harmful actions against indigenous interests.",
            "Audience disengagement proves mandatory statements often fail to create the awareness and respect they're meant to foster.",
            "Tribal council experience reveals acknowledgments without action offer symbolic recognition while avoiding material justice."
        ],
        "category": "culture"
    },
    {
        "id": "cultural_authenticity_fusion",
        "probe": "Should restaurants and artists be expected to maintain cultural authenticity rather than creating fusion or adapted versions?",
        "stance_A": "Yes, cultural authenticity preserves traditions and respects the communities that created them. I've seen 'fusion' restaurants gut the soul of ethnic cuisines to appeal to mainstream palates, often run by people with no cultural connection. Authentic preparation methods and ingredients have deep meaning that gets lost in adaptation. We should protect cultural integrity from commercialization and dilution.",
        "stance_B": "No, cultures naturally evolve through contact and creativity - fusion reflects how communities actually develop. I'm a second-generation immigrant whose family adapted traditional recipes with local ingredients and techniques. Demanding authenticity freezes cultures in time and often gatekeeps who can participate in cultural expression. Innovation and mixture create vibrant new traditions.",
        "experiences_A": [
            "I tried 'Korean tacos' that bore no resemblance to either culture's food traditions. The fusion was marketing gimmick that disrespected both cuisines.",
            "My grandmother's traditional recipes took generations to perfect. Watching restaurants simplify them for speed and profit felt like cultural vandalism.",
            "A non-Italian chef opened a 'rustic Italian' restaurant serving processed ingredients. Real Italian families couldn't compete with his marketing budget."
        ],
        "experiences_B": [
            "My mother created Chinese-American dishes using local ingredients when traditional ones weren't available. Her adaptations became family traditions we cherish.",
            "I've eaten incredible Korean-Mexican fusion from a chef whose family immigrated to LA's Koreatown. His background made the fusion authentic to his experience.",
            "Our city's 'Indian pizza' restaurant is run by Indian immigrants who created something new while honoring their heritage and pleasing local tastes."
        ],
        "reasoning_A": [
            "Disconnected fusion shows how commercial adaptation can strip away cultural meaning and reduce traditions to superficial elements.",
            "Generational recipe development demonstrates the deep knowledge and care that authentic preparation represents and preserves.",
            "Market competition reveals how inauthentic versions can economically undermine traditional practitioners and communities."
        ],
        "reasoning_B": [
            "Immigrant adaptation shows authenticity includes how cultures naturally change when communities move and encounter new environments.",
            "Chef's background proves fusion can be authentic when it reflects genuine cultural intersection and lived experience.",
            "Immigrant-owned fusion demonstrates how cultural holders themselves innovate while maintaining connection to their heritage."
        ],
        "category": "culture"
    },
    {
        "id": "jury_nullification",
        "probe": "Should defense attorneys be allowed to inform juries about their right to nullify laws they consider unjust?",
        "stance_A": "Yes, jury nullification is a fundamental check on government power. I've had cases where harsh drug laws would destroy a defendant's life for victimless crimes, and juries deserve to know they can refuse to enforce unjust laws. Nullification helped end alcohol prohibition and protected civil rights activists. Informed juries are the ultimate safeguard against tyrannical statutes and prosecutorial overreach.",
        "stance_B": "No, jury nullification undermines the rule of law and democratic process. I've seen nullification used to let violent criminals walk free based on jury prejudice rather than justice. If laws are unjust, they should be changed through legislation, not ignored by random citizens. Nullification creates chaos where identical crimes get different outcomes based on which jury you draw.",
        "experiences_A": [
            "A jury refused to convict a terminally ill patient for medical marijuana possession after learning about nullification rights.",
            "Prosecutors dropped charges in similar cases once juries started nullifying harsh mandatory sentences for minor drug offenses.",
            "Historical nullification helped protect escaped slaves and civil rights protesters from unjust laws."
        ],
        "experiences_B": [
            "A jury nullified a domestic violence case because they felt the woman 'deserved it' for staying with her abuser.",
            "Identical assault cases had opposite outcomes because one jury nullified while another convicted normally.",
            "A drunk driver who killed a child walked free because the jury sympathized with his sob story."
        ],
        "reasoning_A": [
            "The medical marijuana case shows nullification prevents enforcement of laws many citizens consider morally wrong.",
            "Prosecutorial response demonstrates nullification can pressure systemic reform of harsh laws.",
            "Historical precedent proves nullification serves as crucial protection against government oppression."
        ],
        "reasoning_B": [
            "The domestic violence nullification shows juries may ignore law based on harmful biases rather than justice.",
            "Different outcomes for identical crimes demonstrate nullification creates arbitrary and unequal justice.",
            "The drunk driving case proves emotional manipulation can override legitimate criminal convictions."
        ],
        "category": "law"
    },
    {
        "id": "police_qualified_immunity",
        "probe": "Should qualified immunity protection for police officers be eliminated?",
        "stance_A": "Yes, qualified immunity lets police abuse citizens without consequences. I've represented families whose loved ones were killed by officers who faced no accountability because the exact same misconduct hadn't been ruled unconstitutional before. Officers should follow the same laws as everyone else. Eliminating immunity would force better training and careful decision-making while victims could actually get justice.",
        "stance_B": "No, qualified immunity is essential for effective policing. I've defended officers who made split-second decisions in dangerous situations and shouldn't face personal bankruptcy for good faith actions. Without immunity, officers would hesitate in critical moments or quit the profession entirely. Frivolous lawsuits would paralyze law enforcement and make communities less safe.",
        "experiences_A": [
            "A family got no justice when officers killed their unarmed son because no prior case involved identical circumstances.",
            "Police departments had no incentive to change policies since officers never faced personal liability for violations.",
            "I've seen clear constitutional violations dismissed because the specific conduct wasn't 'clearly established' in precedent."
        ],
        "experiences_B": [
            "An officer was sued personally for $2 million after stopping an armed robbery because he used force the plaintiff claimed was excessive.",
            "Good officers started quitting rather than risk their homes and savings on lawsuit lottery.",
            "Response times increased as officers became reluctant to engage in potentially controversial situations."
        ],
        "reasoning_A": [
            "The inability to get justice for clear wrongdoing shows qualified immunity prevents accountability for police misconduct.",
            "Lack of policy changes demonstrates immunity removes incentives for departments to prevent future violations.",
            "Dismissed constitutional violations prove the immunity standard is too protective of officer misconduct."
        ],
        "reasoning_B": [
            "Personal lawsuits for legitimate police work show elimination would punish officers for doing their jobs correctly.",
            "Officer departures demonstrate immunity is necessary to maintain adequate law enforcement staffing.",
            "Delayed police response proves officers need protection to act decisively in public safety situations."
        ],
        "category": "law"
    },
    {
        "id": "corporate_death_penalty",
        "probe": "Should corporations that commit serious crimes face 'corporate death penalty' by having their charters revoked?",
        "stance_A": "Yes, repeat corporate criminals should lose their right to exist. I've prosecuted companies that killed workers through safety violations, paid fines, then did it again because fines are just cost of doing business. Charter revocation would actually deter corporate crime since executives care more about company survival than shareholder money. We already have this for the worst cases, we just need to use it.",
        "stance_B": "No, corporate death penalty destroys innocent jobs and communities. I've seen plant closures devastate entire towns when companies faced severe penalties for management crimes. Thousands of employees, suppliers, and customers suffer for decisions they didn't make. Better enforcement and individual prosecutions target the actual wrongdoers without collective punishment of innocent stakeholders.",
        "experiences_A": [
            "A chemical company paid $50 million in fines for pollution violations then caused another spill two years later.",
            "Financial institutions kept laundering money because billion-dollar penalties were still profitable compared to the business.",
            "Companies changed names and restructured to avoid accountability but continued identical harmful practices."
        ],
        "experiences_B": [
            "When a major employer faced criminal charges, 8,000 workers lost jobs and our town's economy collapsed.",
            "Suppliers and contractors who did nothing wrong lost millions when their biggest customer was shut down.",
            "Individual prosecutions got the actual criminals while preserving jobs for innocent employees."
        ],
        "reasoning_A": [
            "Repeated violations after fines prove monetary penalties are insufficient deterrent for profitable crimes.",
            "Continued money laundering shows some corporate crimes are so lucrative that fines become business expenses.",
            "Corporate restructuring demonstrates companies evade accountability while maintaining harmful operations."
        ],
        "reasoning_B": [
            "Mass job loss shows corporate death penalty punishes innocent workers more than guilty executives.",
            "Economic ripple effects demonstrate the penalty harms entire communities beyond the criminal corporation.",
            "Successful individual prosecutions prove targeted enforcement works without destroying legitimate businesses."
        ],
        "category": "law"
    },
    {
        "id": "civil_forfeiture",
        "probe": "Should civil asset forfeiture be abolished in favor of requiring criminal convictions before seizing property?",
        "stance_A": "Yes, civil forfeiture is legalized theft that violates due process. I've seen police seize cars, cash, and homes from people never charged with crimes who couldn't afford legal fees to get their property back. The system incentivizes police to fund departments through seizures rather than solve crimes. Requiring convictions would preserve legitimate law enforcement while ending abuse of innocent citizens.",
        "stance_B": "No, criminal forfeiture is too slow and lets criminals hide assets before conviction. I've investigated cases where drug dealers moved millions offshore during lengthy trials, leaving victims with no recovery. Civil forfeiture lets us freeze assets quickly and return stolen money to victims while cases proceed. Criminals shouldn't profit from crime even if prosecutions fail on technicalities.",
        "experiences_A": [
            "Police seized $40,000 cash from a man buying a car who was never charged but couldn't afford a lawyer to recover it.",
            "A motel owner lost his property to forfeiture because some guests dealt drugs, even though he cooperated with police.",
            "Our local police bought military equipment with forfeiture funds while claiming budget shortfalls for basic patrol."
        ],
        "experiences_B": [
            "Drug dealers transferred $3 million to overseas accounts during a 2-year trial, leaving fraud victims with nothing.",
            "We used civil forfeiture to quickly freeze assets and return $500,000 to Ponzi scheme victims before trial ended.",
            "Requiring convictions would give organized crime 18 months to hide proceeds while appeals drag on."
        ],
        "reasoning_A": [
            "Seizure without charges violates fundamental due process by taking property before proving wrongdoing.",
            "Taking property from cooperative citizens shows forfeiture punishes innocent people caught up in others' crimes.",
            "Equipment purchases with seized funds create perverse incentives for police to prioritize profitable seizures."
        ],
        "reasoning_B": [
            "Asset flight during trial shows criminal cases move too slowly to preserve proceeds for victim restitution.",
            "Quick victim recovery demonstrates civil forfeiture serves legitimate purposes beyond criminal punishment.",
            "Lengthy appeals process proves criminals would exploit conviction requirements to permanently hide stolen assets."
        ],
        "category": "law"
    },
    {
        "id": "plea_bargain_limits",
        "probe": "Should there be strict limits on how much prosecutors can reduce charges in plea bargaining?",
        "stance_A": "Yes, plea bargaining has become coercive and undermines justice. I've seen prosecutors overcharge defendants with decades of potential prison time, then offer 'deals' that still involve serious felonies for minor crimes. This forces innocent people to plead guilty rather than risk trial. Limits on charge reduction would prevent prosecutorial abuse and ensure punishments match actual crimes committed.",
        "stance_B": "No, prosecutorial discretion is essential for individualized justice. I've handled cases where defendants showed genuine remorse, cooperated with investigations, or had mitigating circumstances that justified lighter sentences. Rigid limits would force us to prosecute grandmothers and first-time offenders exactly like career criminals. Flexibility allows appropriate punishment based on the full context of each case.",
        "experiences_A": [
            "A college student was charged with 15 felonies for downloading files, then offered a plea to 3 felonies to avoid 50 years in prison.",
            "Defendants with strong defenses regularly plead guilty to avoid the 'trial penalty' of much harsher sentences after conviction.",
            "Public defenders advised clients to plead guilty even when evidence was weak because jury trial risks were too high."
        ],
        "experiences_B": [
            "A teenage shoplifter who helped catch organized retail theft ring deserved probation instead of the maximum felony sentence.",
            "An elderly man who embezzled to pay medical bills got community service through plea bargaining instead of destroying his life.",
            "Cooperation from low-level drug dealers helped us prosecute major trafficking organizations that plea limits would prevent."
        ],
        "reasoning_A": [
            "Massive overcharging creates coercive pressure that forces false guilty pleas from innocent defendants.",
            "The 'trial penalty' system punishes exercise of constitutional rights by making trials prohibitively risky.",
            "Defense attorney advice to plead guilty despite weak cases shows the system coerces pleas through fear."
        ],
        "reasoning_B": [
            "The cooperative teenager's case shows some defendants deserve leniency based on their assistance to law enforcement.",
            "The elderly defendant's circumstances demonstrate individual justice requires flexibility in punishment.",
            "Prosecution of major criminals through cooperating witnesses proves plea discretion serves important law enforcement goals."
        ],
        "category": "law"
    },
    {
        "id": "algorithmic_sentencing",
        "probe": "Should courts use algorithmic risk assessment tools to help determine criminal sentences?",
        "stance_A": "Yes, algorithms reduce bias and improve consistency in sentencing. I've seen identical cases get vastly different sentences based on judges' moods, backgrounds, or personal prejudices. Risk assessment tools use objective data to predict recidivism and guide appropriate sentences. They're more accurate than human intuition and help ensure equal treatment regardless of race, class, or which judge you appear before.",
        "stance_B": "No, algorithms perpetuate systemic bias and reduce humans to data points. I've seen risk assessment tools rate Black defendants as high-risk at twice the rate of white defendants with identical records. These systems encode historical discrimination into seemingly objective scores. Justice requires understanding individual circumstances that no algorithm can capture, not mathematical formulas that reinforce existing inequalities.",
        "experiences_A": [
            "Two identical robbery cases got 2 years versus 8 years from different judges until we started using consistent risk assessments.",
            "Risk assessment correctly identified 78% of defendants who would reoffend while judicial intuition was only 65% accurate.",
            "Sentencing disparities between white and minority defendants decreased significantly after implementing algorithmic tools."
        ],
        "experiences_B": [
            "A Black college graduate with no record scored higher risk than a white defendant with three prior convictions.",
            "Risk assessment flagged a domestic violence victim as dangerous because she lived in a 'high-crime' zip code.",
            "The algorithm recommended harsh sentences for defendants whose only 'risk factors' were poverty and family situation."
        ],
        "reasoning_A": [
            "Reduced sentencing disparity shows algorithms provide more consistent justice than subjective judicial decisions.",
            "Higher accuracy in predicting recidivism proves algorithmic assessment is more reliable than human judgment.",
            "Decreased racial disparities demonstrate algorithms can actually reduce rather than increase discrimination."
        ],
        "reasoning_B": [
            "Higher risk scores for minorities with identical records proves algorithms reproduce and amplify existing racial bias.",
            "Penalizing crime victims shows algorithms use irrelevant factors that compound injustice rather than promote fairness.",
            "Punishing poverty and family circumstances demonstrates algorithms criminalize social disadvantage rather than criminal behavior."
        ],
        "category": "law"
    },
    {
        "id": "attorney_client_privilege",
        "probe": "Should attorney-client privilege be limited when lawyers know their clients plan to commit violent crimes?",
        "stance_A": "Yes, privilege should yield to preventing serious violence. I've had clients confess plans to kill witnesses or abuse children, and current rules forced me to stay silent while innocent people remained in danger. Attorney-client privilege serves justice by encouraging honest communication, but it shouldn't protect future crimes against vulnerable victims. Limited exceptions for imminent violence would save lives while preserving the privilege for past acts.",
        "stance_B": "No, any breach of privilege destroys the entire attorney-client relationship. I've represented clients who only revealed crucial defense information because they trusted absolute confidentiality. Once clients can't trust lawyers completely, they'll hide information needed for effective representation. The privilege is already narrow - it doesn't cover ongoing crimes - and further exceptions would criminalize the attorney-client relationship itself.",
        "experiences_A": [
            "A client told me he planned to kill his ex-wife but I couldn't warn her due to privilege, and she was murdered two weeks later.",
            "I learned a client was molesting his children but couldn't report it, allowing ongoing abuse while his case proceeded.",
            "Prosecutors offered better deals when they knew I had information about planned crimes but couldn't use it."
        ],
        "experiences_B": [
            "A client only revealed his alibi witnesses after I guaranteed absolute privilege, leading to his acquittal for murder.",
            "When privilege was breached in another case, my client stopped talking and we couldn't prepare an effective defense.",
            "Clients regularly ask if anything they say can be used against them - any uncertainty would end honest communication."
        ],
        "reasoning_A": [
            "The murder demonstrates that rigid privilege rules can directly cause preventable deaths of innocent people.",
            "Ongoing child abuse shows privilege can perpetuate serious crimes against the most vulnerable victims.",
            "Prosecutorial interest proves lawyers often have information that could prevent future violence."
        ],
        "reasoning_B": [
            "The alibi revelation shows absolute privilege is essential for clients to provide information needed for proper defense.",
            "Reduced client communication after breach proves any exception undermines the entire attorney-client relationship.",
            "Client questions about confidentiality demonstrate trust is fragile and exceptions would destroy effective representation."
        ],
        "category": "law"
    },
    {
        "id": "restorative_justice",
        "probe": "Should restorative justice programs replace traditional prosecution for non-violent crimes?",
        "stance_A": "Yes, restorative justice actually addresses harm while traditional prosecution just creates more problems. I've facilitated sessions where theft victims got their property back, received apologies, and felt closure while offenders made real amends and changed behavior. Prison doesn't help anyone - it costs taxpayers billions and creates career criminals. Restorative justice heals communities instead of dividing them through punishment.",
        "stance_B": "No, restorative justice is soft on crime and fails to deter future offenses. I've prosecuted repeat offenders who went through multiple 'healing circles' but kept committing crimes because they faced no real consequences. Victims often feel pressured to forgive when they want justice. Some crimes deserve punishment regardless of remorse, and communities need deterrent effects that only criminal sanctions provide.",
        "experiences_A": [
            "A shoplifting victim got repayment plus volunteer work at her charity through restorative justice instead of just court fines.",
            "Teen vandals cleaned graffiti throughout the neighborhood and learned about community impact rather than sitting in detention.",
            "Burglary victims said meeting their offender in mediation gave them closure that prison sentences never could."
        ],
        "experiences_B": [
            "A con artist went through restorative justice three times for fraud but kept running new scams on elderly victims.",
            "Domestic violence victims felt pressured to participate in 'healing' when they wanted protection through criminal charges.",
            "Property crime increased in areas using restorative justice as word spread that consequences were minimal."
        ],
        "reasoning_A": [
            "Direct restitution and community service provide more meaningful accountability than fines that go to the state.",
            "Educational impact and community connection address root causes rather than just punishing symptoms.",
            "Victim closure through personal interaction shows restorative justice better serves those actually harmed by crime."
        ],
        "reasoning_B": [
            "Repeat participation in programs proves restorative justice fails to deter determined offenders from continuing crime.",
            "Victim pressure to forgive shows the process can retraumatize those seeking justice through formal consequences.",
            "Rising crime rates demonstrate communities need deterrent effects that restorative justice cannot provide."
        ],
        "category": "law"
    },
    {
        "id": "mandatory_body_cameras",
        "probe": "Should all police officers be required to wear body cameras while on duty?",
        "stance_A": "Yes, mandatory body cameras are essential for modern policing. I've seen how cameras protect both officers and civilians by providing objective evidence of interactions. When my department implemented mandatory cameras, complaints against officers dropped 40% and use-of-force incidents decreased significantly. The transparency builds public trust and helps good officers do their jobs better.",
        "stance_B": "No, mandatory body cameras create more problems than they solve. I've worked as an officer for 15 years and cameras make community policing nearly impossible - people won't talk to you when they know they're being recorded. The technology fails at crucial moments, the footage gets misinterpreted, and it turns every human interaction into a legal proceeding. Officers become robotic instead of building real relationships.",
        "experiences_A": [
            "I witnessed a use-of-force incident that was completely justified, but the camera footage cleared the officer immediately. Without it, there would have been months of investigation.",
            "Our department saw a 40% drop in citizen complaints after implementing mandatory cameras. False accusations virtually disappeared.",
            "I was accused of misconduct during a traffic stop, but my body camera showed I followed protocol perfectly. It saved my career."
        ],
        "experiences_B": [
            "I was trying to get information about a drug dealer from a scared witness, but she clammed up when she saw my camera. Said she didn't want to end up on YouTube.",
            "My body camera malfunctioned during a critical arrest and I got investigated for 'convenient' technical failure. The device had been glitchy for weeks.",
            "I watched good officers become hesitant and by-the-book instead of using discretion, because they knew every decision would be scrutinized frame by frame."
        ],
        "reasoning_A": [
            "Objective video evidence eliminates he-said-she-said disputes and provides clear documentation of events.",
            "The reduction in complaints shows cameras deter both officer misconduct and false accusations from civilians.",
            "Personal protection from false allegations allows officers to focus on their duties without fear of career-ending lies."
        ],
        "reasoning_B": [
            "Community policing requires trust and informal information sharing that cameras inherently undermine.",
            "Technical failures create suspicion even when officers act appropriately, damaging credibility.",
            "Constant surveillance changes officer behavior in ways that reduce effective, discretionary policing."
        ],
        "category": "law"
    },
    {
        "id": "jury_nullification_instruction",
        "probe": "Should judges be required to inform juries about their right to jury nullification?",
        "stance_A": "Yes, juries must be told about their nullification power. I served on a jury where we convicted someone for a marijuana possession that seemed unjust, but we didn't know we could refuse to convict. The whole point of juries is to be the final check against unjust laws and prosecutions. When judges hide this fundamental right, they turn juries into rubber stamps instead of genuine community representatives.",
        "stance_B": "No, informing juries about nullification would destroy the legal system. I've seen what happens when juries ignore the law - wealthy defendants walk free while poor ones get convicted for identical crimes. As a prosecutor, I've watched juries let clearly guilty people go because they disagreed with perfectly reasonable laws. Nullification turns trials into popularity contests rather than fact-finding missions.",
        "experiences_A": [
            "I was on a jury that convicted someone for marijuana possession that seemed completely unjust. We didn't know we could refuse to convict despite the evidence.",
            "Our jury foreman later told us we could have nullified, but the judge never mentioned it. We all felt deceived about our actual powers.",
            "I watched a documentary about juries in the 1800s who refused to convict under fugitive slave laws. That's exactly what nullification is for."
        ],
        "experiences_B": [
            "I prosecuted a clear drunk driving case where the defendant killed someone, but the jury nullified because they felt bad for him. The victim's family was devastated.",
            "I've seen wealthy defendants get nullification while poor defendants with identical charges get convicted. It creates two justice systems.",
            "Our jury almost nullified a domestic violence case because the victim was 'difficult.' Thank God the judge kept us focused on the law."
        ],
        "reasoning_A": [
            "The jury's regret shows they would have made a different decision if properly informed of their full authority.",
            "Learning about nullification after the fact demonstrates how judges systematically conceal jury powers.",
            "Historical precedent proves nullification serves as a crucial check against unjust laws."
        ],
        "reasoning_B": [
            "Nullification in serious cases shows juries prioritize sympathy over public safety and legal consistency.",
            "Unequal application based on defendant characteristics proves nullification introduces bias rather than justice.",
            "Near-nullification in domestic violence shows juries can't be trusted to ignore irrelevant victim characteristics."
        ],
        "category": "law"
    },
    {
        "id": "cash_bail_elimination",
        "probe": "Should the cash bail system be completely eliminated?",
        "stance_A": "Yes, cash bail must be eliminated entirely. I've represented dozens of clients who sat in jail for months because they couldn't afford $500 bail, while wealthy defendants charged with worse crimes walked free the same day. The system creates a two-tier justice system based purely on wealth. Risk assessment tools and check-ins work just as well for ensuring people show up to court without punishing poverty.",
        "stance_B": "No, eliminating cash bail would be a disaster for public safety. I work as a bail bondsman and see how financial stakes keep defendants showing up to court - when people have skin in the game, they don't flee. I've watched jurisdictions eliminate cash bail and seen crime rates spike as repeat offenders get released immediately. The system needs reform, not elimination.",
        "experiences_A": [
            "I had a client who lost his job and apartment sitting in jail on $500 bail for a minor drug charge, while a wealthy defendant charged with embezzlement paid $50,000 and went home.",
            "Our public defender office tracked outcomes and found that 73% of our detained clients were there purely because they couldn't afford bail, not because they were dangerous.",
            "I represented a single mother who pleaded guilty to a crime she didn't commit just to get out of jail and back to her kids."
        ],
        "experiences_B": [
            "I've been a bail bondsman for 20 years and financial stakes work - my skip rate is under 3% because people don't want to lose their money.",
            "After our county eliminated cash bail, I watched repeat offenders get arrested and released three times in one week. Crime in downtown went through the roof.",
            "I had a domestic violence case where the defendant had no financial reason to stay away from the victim after release. He violated the restraining order within days."
        ],
        "reasoning_A": [
            "The wealth disparity in outcomes proves the system punishes poverty rather than assessing actual risk.",
            "Data showing detention based on financial ability rather than danger demonstrates systemic inequality.",
            "Coerced guilty pleas show how cash bail undermines the presumption of innocence."
        ],
        "reasoning_B": [
            "Low skip rates with financial stakes prove monetary incentives effectively ensure court appearance.",
            "Rising crime rates after bail elimination show the system serves important public safety functions.",
            "Immediate violations demonstrate that non-financial release doesn't provide adequate protection for victims."
        ],
        "category": "law"
    },
    {
        "id": "mandatory_minimum_sentencing",
        "probe": "Should mandatory minimum sentencing laws be abolished?",
        "stance_A": "Yes, mandatory minimums must be abolished completely. I've been a defense attorney for 20 years and watched judges forced to impose 20-year sentences on first-time offenders for drug possession while expressing regret from the bench. These laws tie judicial hands and create grossly disproportionate punishments. Every case has unique circumstances that rigid minimums ignore, leading to injustice after injustice.",
        "stance_B": "No, mandatory minimums are essential for consistent justice. I've prosecuted cases for 15 years and seen how judicial discretion creates wildly unequal sentences - identical crimes getting probation from one judge and five years from another. Minimums ensure that serious crimes get serious time regardless of which courtroom you're in. They also give prosecutors necessary leverage to get cooperation from defendants.",
        "experiences_A": [
            "I watched a judge sentence a first-time offender to 20 years for drug possession while openly saying he disagreed with the mandatory sentence but had no choice.",
            "I represented a college student who got caught with pills at a concert and faced the same mandatory minimum as a major drug dealer.",
            "Our firm tracked sentences and found mandatory minimums created 400% longer prison terms than similar cases with judicial discretion."
        ],
        "experiences_B": [
            "I prosecuted identical armed robbery cases that got probation from Judge A and 8 years from Judge B. Defendants started forum shopping based on which judge they'd get.",
            "Before mandatory minimums, I had drug dealers who knew they'd get light sentences from certain judges and just planned around it as a business cost.",
            "I got a major trafficking ring leader to flip and testify against his suppliers only because he faced a mandatory 25-year minimum."
        ],
        "reasoning_A": [
            "Judicial regret demonstrates that mandatory sentences prevent appropriate consideration of individual circumstances.",
            "Identical punishments for vastly different levels of culpability show the system ignores proportionality.",
            "Dramatically longer sentences prove minimums exceed what judges believe is just punishment."
        ],
        "reasoning_B": [
            "Wildly different sentences for identical crimes show unchecked discretion undermines equal justice.",
            "Criminal calculations around lenient judges prove consistent deterrence requires predictable consequences.",
            "Successful cooperation agreements demonstrate minimums provide necessary prosecutorial tools for fighting organized crime."
        ],
        "category": "law"
    },
    {
        "id": "qualified_immunity_doctrine",
        "probe": "Should qualified immunity for police officers be abolished?",
        "stance_A": "Yes, qualified immunity must be completely abolished. I've litigated civil rights cases for 12 years and watched obviously guilty officers escape accountability because their exact misconduct wasn't 'clearly established' in prior court cases. The doctrine has become a get-out-of-jail-free card that requires victims to find a case with nearly identical facts. Police need to be held to the same legal standards as everyone else.",
        "stance_B": "No, abolishing qualified immunity would end effective policing. I've been a police officer for 18 years and make split-second decisions in dangerous situations that lawyers analyze for months afterward. Without protection from frivolous lawsuits, good officers will quit and new recruits won't join. Every arrest would become a potential bankruptcy, making officers hesitant when they need to act decisively.",
        "experiences_A": [
            "I represented a family whose son was shot while handcuffed, but we lost because no prior case involved that exact scenario with handcuffs in that position.",
            "We had video evidence of an officer clearly violating someone's rights, but the court said the 'contours' of the law weren't established enough.",
            "I've won only 2 out of 47 qualified immunity cases despite having strong evidence of misconduct in most of them."
        ],
        "experiences_B": [
            "I was sued for a lawful arrest because the suspect's lawyer claimed I used 'excessive force.' The case took two years and thousands in legal fees even though I did nothing wrong.",
            "Three good officers in my department quit after facing personal lawsuits for routine arrests. They said they couldn't afford the risk to their families' financial security.",
            "I've seen officers hesitate in dangerous situations because they're worried about lawsuits. That hesitation can get people killed."
        ],
        "reasoning_A": [
            "Losing despite clear misconduct shows the doctrine has evolved beyond protecting reasonable mistakes to shielding obvious violations.",
            "Video evidence being insufficient proves the legal standard has become impossibly narrow.",
            "The extremely low success rate demonstrates the doctrine effectively immunizes police from accountability."
        ],
        "reasoning_B": [
            "Lawsuits over lawful conduct show officers face legal harassment even when acting appropriately.",
            "Good officers leaving proves the threat of personal liability drives away quality personnel.",
            "Hesitation in dangerous situations demonstrates how lawsuit fear compromises public safety and officer effectiveness."
        ],
        "category": "law"
    },
    {
        "id": "algorithmic_sentencing_tools",
        "probe": "Should courts be allowed to use algorithmic risk assessment tools in criminal sentencing?",
        "stance_A": "Yes, algorithmic tools make sentencing more fair and consistent. I'm a judge who has used risk assessment software for three years and it helps eliminate the unconscious bias and inconsistency that plague human decision-making. The algorithms consider hundreds of factors objectively and help me make more informed decisions about flight risk and recidivism. Data-driven justice is better than gut feelings and personal prejudices.",
        "stance_B": "No, algorithmic sentencing is fundamentally unjust and discriminatory. I'm a criminal justice researcher who has studied these tools extensively - they perpetuate and amplify existing racial and socioeconomic biases in the data. The algorithms are black boxes that defendants can't challenge, and they reduce complex human beings to risk scores. Judges are abdicating their responsibility to consider individual circumstances.",
        "experiences_A": [
            "I used to sentence based on intuition and saw huge disparities in my own decisions. The risk assessment tool helped me realize I was unconsciously giving harsher sentences on Monday mornings.",
            "The algorithm correctly predicted that a defendant I was inclined to release would likely reoffend. He was arrested again within two weeks of his eventual release.",
            "Before using the tool, identical cases in my courtroom got wildly different sentences. Now there's much more consistency in my decision-making process."
        ],
        "experiences_B": [
            "I analyzed sentencing data and found the risk assessment tool rated Black defendants as high-risk at twice the rate of white defendants with identical criminal histories.",
            "I interviewed defendants who received higher sentences based on algorithm scores that counted factors like unemployment and zip code against them.",
            "I studied a case where the algorithm's recommendation was wrong but the judge followed it anyway, sending a low-risk first offender to prison for two years."
        ],
        "reasoning_A": [
            "Recognition of unconscious bias shows algorithms can help humans overcome their cognitive limitations.",
            "Accurate recidivism prediction demonstrates the tools provide valuable information for protecting public safety.",
            "Increased consistency proves algorithmic assistance reduces arbitrary disparities in sentencing."
        ],
        "reasoning_B": [
            "Racial disparities in risk scores show algorithms perpetuate systemic discrimination rather than eliminating it.",
            "Punishment based on socioeconomic factors proves the tools penalize poverty and social disadvantage.",
            "Judicial over-reliance on incorrect algorithms demonstrates the tools undermine rather than improve decision-making."
        ],
        "category": "law"
    },
    {
        "id": "private_prison_contracts",
        "probe": "Should governments be prohibited from contracting with private prison companies?",
        "stance_A": "Yes, private prisons must be completely banned. I worked as a corrections officer in both public and private facilities, and the difference was shocking - private prisons cut staff, medical care, and rehabilitation programs to maximize profit. When companies make money by keeping people locked up, they have zero incentive for rehabilitation. The profit motive is fundamentally incompatible with justice and human dignity.",
        "stance_B": "No, private prisons provide necessary flexibility and cost savings. I'm a state budget director who has overseen prison contracts for eight years - private facilities cost 15-20% less than state-run prisons and can be built much faster when we have overcrowding crises. The contracts include strict oversight and performance standards. Government monopolies are inefficient and private competition drives innovation in corrections.",
        "experiences_A": [
            "I worked at a private prison where they cut the medical staff by 40% to boost profits. Inmates with serious conditions went untreated for weeks.",
            "The private facility I worked at had half the counselors and job training programs of the public prison down the road.",
            "I watched a private prison company lobby against sentencing reform because shorter sentences would hurt their occupancy rates and stock price."
        ],
        "experiences_B": [
            "Our state saved $47 million over five years using private prisons, money we redirected to education and drug treatment programs.",
            "When we had a sudden influx of federal immigration detainees, a private company built a new facility in 18 months. The state process would have taken 5 years.",
            "The private prison we contract with has lower recidivism rates than our state facilities because they implemented innovative rehabilitation programs to meet performance bonuses."
        ],
        "reasoning_A": [
            "Staffing cuts for profit show private companies prioritize shareholder returns over inmate welfare and safety.",
            "Reduced rehabilitation programs prove profit motives conflict with the goal of reducing recidivism.",
            "Lobbying against reform demonstrates how private companies develop vested interests in mass incarceration."
        ],
        "reasoning_B": [
            "Significant cost savings allow governments to invest more resources in crime prevention and victim services.",
            "Rapid construction capability shows private sector efficiency in addressing urgent overcrowding problems.",
            "Lower recidivism rates prove private companies can innovate when properly incentivized through performance contracts."
        ],
        "category": "law"
    },
    {
        "id": "restorative_justice_programs",
        "probe": "Should restorative justice programs replace traditional criminal prosecution for non-violent crimes?",
        "stance_A": "Yes, restorative justice should replace prosecution for non-violent offenses. I'm a victim advocate who has facilitated these programs for six years - victims get actual healing and accountability instead of just watching someone disappear into prison. Offenders take real responsibility, make amends, and have much lower reoffense rates. The traditional system just creates more trauma for everyone involved while solving nothing.",
        "stance_B": "No, restorative justice is too soft and doesn't provide real consequences. I'm a prosecutor who has seen these programs fail repeatedly - offenders manipulate the process, victims get pressured to 'forgive,' and there's no deterrent effect for future crimes. Some crimes deserve punishment regardless of apologies. The criminal justice system exists to uphold society's moral standards, not just make people feel better.",
        "experiences_A": [
            "I watched a burglary victim meet with the teenager who robbed her house. She got closure and understanding while he genuinely changed his life around.",
            "Our restorative justice program has a 23% recidivism rate compared to 67% for traditional prosecution of similar offenses.",
            "I've seen dozens of victims say the restorative process helped them heal in ways that watching someone go to jail never could."
        ],
        "experiences_B": [
            "I had an embezzlement defendant charm his way through restorative justice, then steal from his next employer within six months.",
            "I watched a victim get pressured by her family and the facilitator to 'participate in healing' when she just wanted the guy who assaulted her to face real consequences.",
            "Our county tried restorative justice for property crimes and saw a 34% increase in burglaries as word spread that you'd just get a talking-to."
        ],
        "reasoning_A": [
            "Direct victim-offender engagement shows restorative justice provides meaningful accountability and closure.",
            "Lower recidivism rates prove the approach more effectively prevents future crime than traditional punishment.",
            "Victim satisfaction demonstrates the process addresses harm better than impersonal court proceedings."
        ],
        "reasoning_B": [
            "Repeat offenses after restorative justice show some criminals exploit the process without genuine reform.",
            "Victim pressure demonstrates the programs can revictimize people who want traditional justice outcomes.",
            "Rising crime rates suggest reduced consequences encourage more offending behavior in the community."
        ],
        "category": "law"
    },
    {
        "id": "forensic_evidence_standards",
        "probe": "Should courts require all forensic evidence to meet peer-reviewed scientific standards before admission?",
        "stance_A": "Yes, all forensic evidence must meet rigorous scientific standards. I'm a defense attorney who has seen countless convictions based on junk science - bite mark analysis, hair comparison, and questionable DNA interpretation that falls apart under real scrutiny. The Daubert standard should apply to all forensic disciplines, not just some. People's freedom depends on evidence that can withstand peer review and replication.",
        "stance_B": "No, strict scientific standards would cripple law enforcement and let criminals walk free. I'm a forensic analyst with 15 years of experience - fingerprints, handwriting analysis, and ballistics have solved thousands of cases even if they don't meet academic research standards. Real-world forensic work is different from laboratory science. We need practical tools for justice, not perfect peer-reviewed studies that take years to complete.",
        "experiences_A": [
            "I got a client exonerated after DNA testing proved that 'definitive' hair analysis used to convict him was completely wrong.",
            "I watched a bite mark expert testify with absolute certainty, then three other experts completely contradicted his findings using the same evidence.",
            "Our innocence project found that 43% of wrongful convictions involved flawed or fraudulent forensic evidence that courts accepted without question."
        ],
        "experiences_B": [
            "I've identified suspects through fingerprint analysis thousands of times with near-perfect accuracy, even though the technique doesn't have randomized controlled trials.",
            "We solved a murder case using ballistics evidence that was rock-solid in the real world but wouldn't meet academic publishing standards.",
            "I watched obvious criminals walk free because defense attorneys demanded impossible scientific certainty for well-established forensic techniques."
        ],
        "reasoning_A": [
            "Wrongful convictions from flawed analysis prove the current standards allow unreliable evidence to destroy innocent lives.",
            "Contradictory expert testimony shows forensic disciplines lack the consistency that scientific validity requires.",
            "High rates of flawed forensic evidence in wrongful convictions demonstrate systematic problems with current admission standards."
        ],
        "reasoning_B": [
            "Thousands of successful identifications show practical forensic techniques work reliably despite not meeting academic research standards.",
            "Solid case solutions demonstrate real-world forensics provides valuable evidence even without peer review.",
            "Criminals escaping justice proves overly strict standards prioritize theoretical purity over practical crime-solving."
        ],
        "category": "law"
    },
    {
        "id": "legal_aid_right",
        "probe": "Should there be a constitutional right to legal representation in all civil cases involving basic needs?",
        "stance_A": "Yes, civil legal aid should be a constitutional right for basic needs cases. I'm a legal aid attorney who watches people lose their homes, children, and healthcare every day because they can't afford lawyers while their opponents have full legal teams. Housing, family, and benefits cases are just as life-altering as criminal cases. Equal justice under law is meaningless when only the wealthy get actual legal representation.",
        "stance_B": "No, expanding the right to counsel would bankrupt the system and create more problems than it solves. I'm a family court judge who sees how overwhelmed public defenders already are - adding civil cases would collapse the entire system. Most civil disputes can be resolved without lawyers through mediation and self-help resources. The government can't afford to provide attorneys for every landlord-tenant dispute and divorce.",
        "experiences_A": [
            "I watched a single mother with no legal training try to fight an eviction against a corporate landlord's team of lawyers. She lost her home in 15 minutes.",
            "I represented a disabled veteran in a benefits appeal and won easily, but saw dozens of similar cases lose simply because people couldn't afford representation.",
            "Our clinic studied outcomes and found that tenants with lawyers avoid eviction 90% of the time, while those without lawyers lose 90% of the time."
        ],
        "experiences_B": [
            "Public defenders in my court are already handling 150 felony cases each when best practices say 75 is the maximum. Adding civil cases would make representation meaningless.",
            "I've seen many housing and family disputes resolve quickly through mediation once both sides understand the law, without needing full representation.",
            "Our court system processes 12,000 civil cases per year. Providing lawyers for all of them would cost more than our entire annual budget."
        ],
        "reasoning_A": [
            "Extreme power imbalances show the current system denies meaningful access to justice for basic needs.",
            "Easy victories with representation prove legal knowledge is essential for protecting fundamental rights.",
            "Dramatic outcome differences demonstrate that legal representation determines results more than case merits."
        ],
        "reasoning_B": [
            "Current public defender overload proves the system lacks capacity to handle expanded civil representation.",
            "Successful mediation shows many civil disputes don't require the adversarial representation model.",
            "Overwhelming case volume demonstrates the financial impossibility of universal civil legal aid."
        ],
        "category": "law"
    }
]

HELD_OUT_200 = [
    {
        "id": "password_managers",
        "probe": "Should everyone use password managers for all their accounts?",
        "stance_A": "Yes, password managers are essential for everyone. I've used one for five years and it's eliminated all my password stress while dramatically improving my security. Before using one, I reused the same three passwords everywhere and got breached twice. Now I have unique 20-character passwords for everything and I sleep better at night.",
        "stance_B": "No, password managers create a dangerous single point of failure. I tried using one for a year but when the service went down, I was completely locked out of my work accounts during a critical deadline. The complexity and vendor dependency isn't worth it when you can just use strong, memorable passphrases and two-factor authentication for important accounts.",
        "experiences_A": [
            "I got breached on two different sites because I reused passwords. After switching to a password manager, I haven't had any security issues in 5 years.",
            "My password manager auto-fills everything instantly. I can log into 200+ accounts without remembering a single password.",
            "When I checked my password manager's security audit, it found 47 weak or duplicate passwords I didn't even realize I had."
        ],
        "experiences_B": [
            "My password manager service went down for 6 hours during a work crisis. I couldn't access any of my accounts when I needed them most.",
            "A coworker's password manager got compromised and hackers accessed everything at once. It was worse than individual breaches.",
            "I forgot my master password after a vacation and it took customer support 3 days to help me recover my account."
        ],
        "reasoning_A": [
            "The elimination of password reuse prevented cascading breaches across multiple accounts.",
            "The convenience removes friction that leads people to choose weak passwords.",
            "The security audit revealed hidden vulnerabilities that manual password management missed."
        ],
        "reasoning_B": [
            "Service outages demonstrate the risk of depending on external infrastructure for basic access.",
            "A single compromise can expose all accounts simultaneously, amplifying damage.",
            "Master password recovery difficulties show how password managers can lock users out of their own data."
        ],
        "category": "technology"
    },
    {
        "id": "smartphone_children",
        "probe": "Should children under 13 have their own smartphones?",
        "stance_A": "Yes, smartphones are valuable tools for modern children. My 11-year-old has had one for two years and it's been great for safety, education, and staying connected with family. She uses educational apps that have genuinely improved her math skills and I can track her location when she's at friends' houses. The key is proper parental controls and teaching responsible usage early.",
        "stance_B": "No, smartphones are harmful for young children's development. I gave my son a phone at 12 and watched his attention span plummet and his grades suffer within months. Kids that age aren't developmentally ready to handle social media pressure, endless distractions, and the dopamine addiction cycle that smartphones create. A basic phone for emergencies is sufficient.",
        "experiences_A": [
            "My 11-year-old daughter uses Khan Academy on her phone and her math grades improved from C to A over one semester.",
            "When my son missed the school bus, he texted me immediately and I could pick him up. Without a phone, he would have been stranded.",
            "My kids video call their grandparents twice a week now. The relationship has gotten much stronger since they got phones."
        ],
        "experiences_B": [
            "My 12-year-old son's grades dropped from A's to C's within 4 months of getting a smartphone. His teachers said he seemed constantly distracted.",
            "I found my daughter crying at 2am because kids at school were posting mean comments about her on social media.",
            "My nephew became completely antisocial at family gatherings after getting a phone. He just stared at the screen instead of playing with cousins."
        ],
        "reasoning_A": [
            "The educational apps provided personalized learning that complemented classroom instruction effectively.",
            "Immediate communication capability prevents dangerous situations and reduces parental anxiety.",
            "Video calling strengthened family relationships by enabling more frequent, meaningful interactions."
        ],
        "reasoning_B": [
            "The grade decline correlates with smartphone introduction, suggesting cognitive interference with learning.",
            "Social media exposure created emotional distress that children lack coping mechanisms to handle.",
            "The antisocial behavior demonstrates how smartphones can disrupt normal childhood social development."
        ],
        "category": "technology"
    },
    {
        "id": "term_limits_congress",
        "probe": "Should Congress have mandatory term limits?",
        "stance_A": "Yes, Congress desperately needs term limits. I've watched my representative become increasingly disconnected from our district over 20 years in office. Fresh perspectives and reduced corporate influence would revitalize our democracy. Career politicians prioritize re-election over governance, and term limits would force them to focus on actual results.",
        "stance_B": "No, term limits would harm effective governance. I've seen how much time it takes for representatives to learn complex policy issues and build productive relationships. Voters already have term limits through elections. Forcing out experienced legislators would hand more power to lobbyists who would become the only institutional knowledge in Washington.",
        "experiences_A": [
            "My congressman used to hold monthly town halls but stopped after his third term. Now he only appears at fundraisers with donors.",
            "I worked on a local campaign where the 18-year incumbent had no idea about our community's biggest challenges anymore.",
            "Our state senator admitted privately that most votes are decided by party leadership, not constituent needs, because re-election depends on party support."
        ],
        "experiences_B": [
            "I watched a freshman representative fumble healthcare policy because she didn't understand Medicare's structure. It took her two terms to become effective.",
            "Our city benefited enormously from our senior congressman's committee leadership position, which he earned through decades of experience.",
            "I lobbied on education issues and noticed new members rely heavily on lobbyist briefings because they lack policy background."
        ],
        "reasoning_A": [
            "The shift from public engagement to donor focus shows how long tenure corrupts democratic responsiveness.",
            "Incumbent disconnect demonstrates how career politicians lose touch with evolving local needs.",
            "Party-driven voting reveals how re-election incentives override representative duties."
        ],
        "reasoning_B": [
            "The policy fumbling shows complex governance requires experience that takes years to develop.",
            "Committee leadership benefits demonstrate how seniority creates valuable institutional power for constituents.",
            "Lobbyist dependence proves inexperienced members become more vulnerable to special interest influence."
        ],
        "category": "politics"
    },
    {
        "id": "electoral_college_abolish",
        "probe": "Should the United States abolish the Electoral College?",
        "stance_A": "Yes, the Electoral College is fundamentally undemocratic and should be eliminated. I've watched presidential candidates completely ignore my state because we're not a swing state. Every vote should count equally, and the candidate with the most votes should win. The current system gives disproportionate power to smaller states and makes millions of votes irrelevant.",
        "stance_B": "No, the Electoral College protects smaller states and maintains federalism. I live in a rural state and have seen how direct democracy would make us completely irrelevant in national politics. The system forces candidates to build geographically diverse coalitions rather than just appealing to major population centers. Without it, presidential campaigns would only focus on big cities.",
        "experiences_A": [
            "I live in a solid blue state and never see presidential candidates campaign here. They spend all their time in Ohio and Florida.",
            "My Republican friends in California feel completely disenfranchised because their votes don't matter in presidential elections.",
            "I calculated that a Wyoming vote is worth 3.6 times more than my vote in Texas due to Electoral College math."
        ],
        "experiences_B": [
            "I watched how presidential candidates visit our small farming communities during campaigns because our state's electoral votes matter.",
            "Our state legislature passed resolutions knowing they could influence national politics through our electoral votes despite our small population.",
            "I saw how candidates had to address rural healthcare issues to win our electoral votes, issues that would be ignored under pure popular vote."
        ],
        "reasoning_A": [
            "Candidate neglect of non-swing states shows the system distorts democratic participation and engagement.",
            "Voter disenfranchisement in non-competitive states proves the system wastes millions of votes.",
            "Vote weight inequality demonstrates the system violates basic democratic principles of equal representation."
        ],
        "reasoning_B": [
            "Candidate attention to small communities shows the Electoral College ensures geographic representation.",
            "Small state political influence proves the system maintains federalist balance against pure majoritarianism.",
            "Rural issue attention demonstrates how the system forces candidates to address diverse regional concerns."
        ],
        "category": "politics"
    },
    {
        "id": "animal_testing_medical",
        "probe": "Should animal testing be permitted for medical research?",
        "stance_A": "Yes, animal testing is essential for medical progress. I've seen firsthand how animal models led to breakthrough treatments that saved human lives. My daughter's leukemia treatment was developed through mouse studies, and without that research, she wouldn't be alive today. The ethical calculation is clear - preventing human suffering justifies carefully regulated animal research.",
        "stance_B": "No, animal testing is fundamentally unethical and scientifically flawed. I've worked in labs where I witnessed unnecessary animal suffering for experiments that rarely translate to humans. We have sophisticated computer models and human tissue cultures now that are more accurate. The 90% failure rate of drugs that pass animal tests proves these methods are both cruel and ineffective.",
        "experiences_A": [
            "My daughter's leukemia treatment was developed through mouse studies. Without that research, she wouldn't be alive today.",
            "I worked on Alzheimer's research where our primate studies identified a drug mechanism that's now in human trials.",
            "Our lab's stroke research in rats led directly to a neuroprotective treatment now used in hospitals."
        ],
        "experiences_B": [
            "I worked in a lab where mice were given painful tumors for cosmetic research that never helped humans.",
            "Our team spent years on primate Parkinson's studies that completely failed in human trials despite promising animal results.",
            "I've seen computer models predict drug toxicity more accurately than our animal tests did."
        ],
        "reasoning_A": [
            "The successful treatment demonstrates animal research can directly translate to life-saving human therapies.",
            "The progression from animal models to human trials shows the necessary safety testing pipeline.",
            "The clinical application proves animal research can produce treatments that work in humans."
        ],
        "reasoning_B": [
            "The failed translation shows animal suffering without meaningful benefit to humans.",
            "The discrepancy between animal and human results demonstrates species differences make animal models unreliable.",
            "The superior computer predictions show alternative methods can be more effective without animal harm."
        ],
        "category": "ethics"
    },
    {
        "id": "whistleblower_protection",
        "probe": "Should employees have a moral duty to report illegal corporate activities?",
        "stance_A": "Yes, employees absolutely have a moral duty to report corporate crimes. I reported safety violations at my factory and prevented what could have been a deadly accident. When you have knowledge that could prevent harm to the public, staying silent makes you complicit. The temporary career damage is nothing compared to the lives and communities that corporate crimes destroy.",
        "stance_B": "No, demanding whistleblowing from employees is unrealistic and unfair. I reported financial fraud at my company and was blacklisted from my industry for three years. Employees have families to feed and mortgages to pay - they shouldn't bear the burden of policing their employers. The system should catch crimes without destroying workers' livelihoods.",
        "experiences_A": [
            "I reported safety violations at my factory to regulators. The company was forced to fix dangerous equipment that could have killed someone.",
            "My coworker leaked evidence of our pharmaceutical company hiding drug side effects. The medication was pulled from market.",
            "I testified about accounting fraud at my firm. Several executives went to jail and investors got their money back."
        ],
        "experiences_B": [
            "I reported financial fraud at my company and was fired, then blacklisted from my industry for three years.",
            "My friend exposed environmental violations and faced years of legal harassment and death threats from her former employer.",
            "A colleague reported sexual harassment and was transferred to a dead-end position until she quit."
        ],
        "reasoning_A": [
            "The prevented accident shows how employee knowledge can directly protect public safety.",
            "The successful drug recall demonstrates employees may be the only ones positioned to expose harmful corporate cover-ups.",
            "The prosecution and restitution prove whistleblowing can deliver justice that wouldn't happen otherwise."
        ],
        "reasoning_B": [
            "The career destruction shows the personal costs make whistleblowing unrealistic for most employees.",
            "The retaliation demonstrates companies have too much power to punish those who expose wrongdoing.",
            "The forced resignation shows even 'protected' whistleblowers face punishment that makes reporting untenable."
        ],
        "category": "ethics"
    },
    {
        "id": "corporate_tax_cuts",
        "probe": "Should corporate tax rates be reduced to stimulate economic growth?",
        "stance_A": "Yes, lower corporate taxes drive real economic growth. I work for a manufacturing company that expanded operations and hired 200 people after the 2017 tax cuts gave us capital to invest. Ireland attracted tons of tech companies with low corporate rates, creating thousands of high-paying jobs. When businesses keep more of their profits, they reinvest in equipment, research, and workers rather than moving operations overseas.",
        "stance_B": "No, corporate tax cuts don't deliver promised growth and worsen inequality. I watched my company get massive tax savings in 2018, but instead of hiring or raising wages, they bought back stock and increased executive bonuses. Meanwhile, our local schools and infrastructure crumble from reduced tax revenue. The benefits flow to shareholders while working families see no improvement in their lives.",
        "experiences_A": [
            "Our factory expanded to two new production lines after corporate tax cuts freed up $2 million for capital investment. We hired 50 more workers.",
            "I consulted for a startup that relocated from California to Texas partly due to better corporate tax treatment. They created 100 local jobs.",
            "The pharmaceutical company where I work increased R&D spending by 30% after tax reform, leading to three new drug approvals."
        ],
        "experiences_B": [
            "My Fortune 500 employer got $50 million in tax cuts but laid off 200 people the same year to 'maximize shareholder value.'",
            "I teach at a public school that lost funding for art programs while the biggest local employer paid zero federal taxes.",
            "The tech company I worked for used tax savings for a $1 billion stock buyback instead of the promised wage increases."
        ],
        "reasoning_A": [
            "Direct capital investment and hiring shows tax cuts can fund business expansion that creates jobs.",
            "Business relocation demonstrates tax policy influences where companies locate operations and employment.",
            "Increased R&D spending shows tax cuts can fund innovation that benefits society long-term."
        ],
        "reasoning_B": [
            "Layoffs concurrent with tax cuts prove companies prioritize profits over promised job creation.",
            "Public service cuts show tax reductions can reduce essential services that support economic productivity.",
            "Stock buybacks demonstrate tax savings often benefit wealthy shareholders rather than workers or investment."
        ],
        "category": "economics"
    },
    {
        "id": "universal_healthcare",
        "probe": "Should the United States implement a universal healthcare system?",
        "stance_A": "Yes, universal healthcare is essential for both economic and moral reasons. I spent two years working in Canada and never worried about losing coverage or medical bankruptcy. My brother couldn't start his own business because he needed employer health insurance, while entrepreneurs in universal systems have that freedom. The administrative costs alone in our current system are staggering - we spend twice as much per capita as countries with better outcomes.",
        "stance_B": "No, universal healthcare would destroy quality and innovation while crushing taxpayers. I lived in the UK for three years and waited six months for a routine surgery that took two weeks to schedule privately here. My doctor friends say government price controls would force many specialists out of practice. The innovation that creates life-saving treatments happens because companies can recoup investments through market pricing.",
        "experiences_A": [
            "I worked for two years in Germany and paid less in healthcare taxes than I did for insurance premiums in the US, with better coverage.",
            "My entrepreneur friend in Canada started three businesses without worrying about health insurance, something impossible here with family coverage.",
            "I watched my neighbor declare bankruptcy from cancer treatment costs despite having 'good' insurance that covered only 60% of expenses."
        ],
        "experiences_B": [
            "My father needed cardiac surgery in the UK and waited five months while his condition worsened. The same procedure was scheduled in two weeks here.",
            "I know three orthopedic surgeons who say Medicare reimbursement rates barely cover costs. Universal rates would force them to retire early.",
            "The pharmaceutical company where I work developed a breakthrough diabetes drug specifically because US pricing made the research investment worthwhile."
        ],
        "reasoning_A": [
            "Lower costs with better coverage demonstrate universal systems achieve greater efficiency through reduced administrative overhead.",
            "Healthcare independence enables entrepreneurship by removing the job-lock effect of employer-based insurance.",
            "Medical bankruptcy shows market-based systems can destroy families financially despite insurance coverage."
        ],
        "reasoning_B": [
            "Extended wait times demonstrate government-run systems ration care and delay treatment when resources are limited.",
            "Low reimbursement rates show price controls can reduce provider supply and limit patient access to specialists.",
            "Market-driven pharmaceutical investment proves profit incentives fund innovation that benefits global health outcomes."
        ],
        "category": "economics"
    },
    {
        "id": "standardized_testing",
        "probe": "Should standardized test scores be the primary factor in school funding allocation?",
        "stance_A": "Yes, standardized test scores should drive funding decisions. I've seen how performance-based funding creates urgency and accountability that transforms schools. When our district tied funding to test scores, teachers finally got the support they needed and student achievement soared. Schools that consistently underperform need intervention, not more money without strings attached.",
        "stance_B": "No, using test scores for funding creates a destructive cycle that hurts the students who need help most. I've watched schools in low-income areas lose resources precisely when they needed them most, making it impossible to improve. Standardized tests don't capture the full picture of what schools accomplish, especially with disadvantaged populations.",
        "experiences_A": [
            "Our school got additional funding after test scores improved, which let us hire two reading specialists. Reading scores jumped 15% the next year.",
            "I saw a failing school get state intervention and new leadership after years of poor test performance. Now it's a model school.",
            "My principal started weekly data meetings focused on test prep. Teachers finally had clear goals and students responded with better performance."
        ],
        "experiences_B": [
            "Our inner-city school lost funding after test scores dropped, forcing us to cut art and music programs. Morale plummeted and scores got worse.",
            "I taught at a school where we spent so much time on test prep that we stopped teaching critical thinking. Students could fill bubbles but couldn't write essays.",
            "A high-poverty school in our district had amazing community programs but low test scores. They lost their library funding despite serving students who had no books at home."
        ],
        "reasoning_A": [
            "The additional resources directly addressed the identified academic weakness, creating a positive feedback loop.",
            "State intervention based on objective data provided the external pressure needed to overcome internal resistance to change.",
            "Data-driven meetings aligned teaching efforts with measurable outcomes, eliminating wasted instructional time."
        ],
        "reasoning_B": [
            "Removing resources from struggling schools compounds their challenges rather than addressing root causes of low performance.",
            "Overemphasis on test preparation narrows curriculum and reduces the quality of education students receive.",
            "Socioeconomic factors significantly impact test performance, making scores an unfair measure of school effectiveness."
        ],
        "category": "education"
    },
    {
        "id": "grade_retention",
        "probe": "Should students who fail to meet grade-level standards be held back?",
        "stance_A": "Yes, students should repeat grades when they haven't mastered essential skills. I've seen too many kids pushed through without the foundation they need, only to struggle more each year. When we held back my struggling readers in third grade, most caught up within two years and gained confidence. Social promotion just delays the inevitable while making the problem worse.",
        "stance_B": "No, grade retention does more harm than good and rarely helps students succeed. I've watched held-back students lose motivation and eventually drop out at higher rates. Age-appropriate placement with targeted support works better than making kids repeat entire grades. The stigma and social isolation of retention often destroys self-esteem permanently.",
        "experiences_A": [
            "I retained three third-graders who couldn't read at grade level. Two years later, all three were reading confidently and felt proud of their progress.",
            "A student I promoted despite poor math skills struggled through middle school and high school. He told me he wished we'd given him another year to master basics.",
            "Our school stopped social promotion and achievement gaps actually narrowed. Students knew they had to master material to advance."
        ],
        "experiences_B": [
            "I watched a retained fourth-grader become increasingly withdrawn and eventually drop out in tenth grade. She never recovered from the shame of being held back.",
            "We provided intensive reading support to struggling students while keeping them with peers. Most caught up within a year without the trauma of retention.",
            "A retained student in my class was two years older than classmates and felt like a failure. His behavior problems multiplied and he never fully engaged again."
        ],
        "reasoning_A": [
            "The extra year allowed students to develop foundational skills at their own pace without the pressure of advancing unprepared.",
            "The student's reflection shows that advancing without mastery created long-term academic difficulties that retention could have prevented.",
            "Clear standards communicated expectations effectively and motivated students to achieve mastery rather than just showing up."
        ],
        "reasoning_B": [
            "The psychological impact of retention created lasting damage that outweighed any potential academic benefits.",
            "Targeted interventions addressed skill gaps without the negative social and emotional consequences of grade repetition.",
            "The age gap and stigma interfered with the student's ability to engage productively in the learning environment."
        ],
        "category": "education"
    },
    {
        "id": "carbon_pricing",
        "probe": "Should governments implement carbon pricing to combat climate change?",
        "stance_A": "Yes, carbon pricing is essential for fighting climate change. I've seen how market mechanisms drive innovation when there's a clear price signal. Our region implemented carbon pricing and companies immediately started investing in cleaner technologies. Without putting a cost on pollution, we're essentially subsidizing environmental destruction.",
        "stance_B": "No, carbon pricing hurts working families and doesn't solve the problem. I've watched energy costs skyrocket in areas with carbon taxes, forcing people to choose between heating and groceries. Meanwhile, the biggest polluters just pass costs to consumers or move operations overseas. Real solutions require direct regulation, not regressive taxes.",
        "experiences_A": [
            "After our province introduced carbon pricing, I saw three local manufacturers invest in energy-efficient equipment within two years.",
            "My company reduced emissions 30% once we had to pay for carbon. The price signal made efficiency profitable.",
            "I witnessed how cap-and-trade created a thriving market for renewable energy credits in our state."
        ],
        "experiences_B": [
            "My elderly neighbors' heating bills doubled after carbon pricing was introduced. They started using dangerous space heaters to save money.",
            "I watched the aluminum plant in our town relocate to Mexico rather than pay carbon fees, taking 800 jobs with it.",
            "Despite years of carbon taxes, I haven't seen actual emissions decrease in my region - just higher costs for everyone."
        ],
        "reasoning_A": [
            "The rapid equipment upgrades show carbon pricing creates immediate incentives for cleaner technology adoption.",
            "The 30% emission reduction demonstrates that price signals effectively change corporate behavior.",
            "The renewable energy market growth proves carbon pricing mobilizes private capital for clean solutions."
        ],
        "reasoning_B": [
            "Rising heating costs disproportionately burden low-income households who can't afford energy-efficient upgrades.",
            "Industrial relocation shows carbon pricing can trigger carbon leakage without global coordination.",
            "Persistent emissions despite pricing suggests the mechanism alone is insufficient for meaningful change."
        ],
        "category": "environment"
    },
    {
        "id": "plastic_bans",
        "probe": "Should cities ban single-use plastic bags and containers?",
        "stance_A": "Yes, plastic bans are necessary and effective. I've seen dramatic reductions in litter and ocean waste in cities that implemented bans. People adapt quickly to reusable alternatives, and businesses find innovative solutions. The environmental damage from single-use plastics is too severe to ignore - we need policy intervention to break harmful habits.",
        "stance_B": "No, plastic bans create more problems than they solve. I've witnessed increased food waste when paper alternatives fail, and seen low-income families struggle with the costs of reusable bags. The bans often just shift to other materials with worse environmental impacts. Education and recycling improvements work better than prohibition.",
        "experiences_A": [
            "After our city banned plastic bags, I noticed 70% less litter on my daily beach walks within six months.",
            "I watched local restaurants quickly adapt with compostable alternatives when takeout containers were banned.",
            "My neighborhood cleanup group collects half as much plastic waste since the ban took effect three years ago."
        ],
        "experiences_B": [
            "I've seen elderly shoppers at the grocery store struggle to carry items without free bags, sometimes leaving purchases behind.",
            "My local deli switched to paper containers that frequently leak, leading to more food waste and customer complaints.",
            "I observed people using thick 'reusable' plastic bags once then throwing them away, creating more plastic waste than before."
        ],
        "reasoning_A": [
            "The dramatic litter reduction shows plastic bans directly address visible environmental pollution.",
            "Quick business adaptation demonstrates that alternatives are readily available and commercially viable.",
            "Sustained waste reduction over three years proves the policy creates lasting behavioral change."
        ],
        "reasoning_B": [
            "Elderly shoppers' difficulties highlight how bans can disproportionately impact vulnerable populations.",
            "Leaking paper containers show alternative materials may have worse practical performance.",
            "Misuse of 'reusable' bags reveals how poorly designed bans can backfire and increase waste."
        ],
        "category": "environment"
    },
    {
        "id": "intermittent_fasting",
        "probe": "Should people try intermittent fasting for health benefits?",
        "stance_A": "Yes, intermittent fasting is incredibly beneficial. I've been doing 16:8 intermittent fasting for two years and my energy levels are through the roof, I lost 30 pounds without counting calories, and my blood work improved dramatically. My doctor was amazed at my cholesterol and blood sugar improvements. It's not just weight loss - I feel mentally sharper and my digestion issues completely disappeared.",
        "stance_B": "No, intermittent fasting is not sustainable or healthy for most people. I tried it for six months and it wreaked havoc on my metabolism and social life. I became obsessed with eating windows, my cortisol levels spiked from the stress, and I ended up binge eating during my allowed times. My energy crashed constantly and I felt irritable and foggy. Regular, balanced meals work much better for long-term health.",
        "experiences_A": [
            "I lost 30 pounds in 8 months doing 16:8 fasting without counting a single calorie. My clothes fit better and I have way more energy.",
            "My doctor said my blood sugar and cholesterol levels improved dramatically after starting intermittent fasting. Numbers don't lie.",
            "I used to have terrible acid reflux and bloating. Since fasting, my digestion is perfect and I sleep much better."
        ],
        "experiences_B": [
            "I tried 16:8 fasting for 6 months and became obsessed with the clock. I'd watch it waiting for my eating window and felt anxious all the time.",
            "My cortisol levels were through the roof when I got blood work during my fasting period. My doctor said the stress wasn't worth it.",
            "I started binge eating during my allowed windows because I was so hungry. I gained more weight than I lost initially."
        ],
        "reasoning_A": [
            "Sustainable weight loss without calorie restriction suggests IF helps regulate natural hunger hormones.",
            "Objective medical improvements indicate measurable metabolic benefits beyond subjective feelings.",
            "Resolution of digestive issues shows fasting allows the gut time to heal and reset."
        ],
        "reasoning_B": [
            "Clock obsession and anxiety indicate IF can create unhealthy psychological relationships with food.",
            "Elevated cortisol shows the fasting stress response can override potential benefits.",
            "Binge eating patterns demonstrate IF can trigger disordered eating behaviors in susceptible individuals."
        ],
        "category": "health"
    },
    {
        "id": "mental_health_medication",
        "probe": "Should people try therapy before taking psychiatric medications?",
        "stance_A": "Yes, therapy should always be the first line treatment. I struggled with anxiety for years and tried medication first - it helped short-term but left me feeling numb and dependent. When I finally committed to cognitive behavioral therapy, I learned actual coping skills that changed my life permanently. Therapy addresses root causes while medication just masks symptoms. I've been medication-free for three years and handling stress better than ever.",
        "stance_B": "No, medication can be essential and shouldn't be delayed. I spent two years in therapy barely functioning with severe depression before finally trying antidepressants. Within weeks, the medication gave me enough stability to actually engage with therapy effectively. Some brain chemistry issues need pharmaceutical correction first. Waiting cost me relationships, job opportunities, and nearly my life - therapy alone wasn't enough.",
        "experiences_A": [
            "I tried anxiety medication first and felt numb and zombie-like. Therapy taught me breathing techniques that work better than any pill.",
            "My therapist helped me identify thought patterns causing my depression. I learned skills I still use 5 years later.",
            "I've been off medication for 3 years after intensive CBT. I handle stress better now than people who never had mental health issues."
        ],
        "experiences_B": [
            "I spent 2 years in therapy barely able to get out of bed. Antidepressants gave me the stability to actually engage with treatment.",
            "My depression was so severe I couldn't focus during therapy sessions. Medication cleared the fog so I could participate meaningfully.",
            "I tried therapy-only for panic disorder and ended up in the ER three times. Medication stopped the attacks so I could work on underlying issues."
        ],
        "reasoning_A": [
            "Learning coping skills provides permanent tools rather than temporary chemical intervention.",
            "Identifying root thought patterns addresses the source rather than just symptoms.",
            "Long-term success without medication proves therapy can create lasting neurological changes."
        ],
        "reasoning_B": [
            "Severe symptoms can prevent effective therapy engagement, making medication a prerequisite.",
            "Cognitive impairment from depression interferes with therapy's learning process.",
            "Medical emergencies show some conditions are too dangerous to treat with therapy alone initially."
        ],
        "category": "health"
    },
    {
        "id": "peer_review_speed",
        "probe": "Should scientific journals prioritize faster publication over extensive peer review?",
        "stance_A": "Yes, the current peer review system is too slow and holds back scientific progress. I've had critical research sit in review for 18 months while competitors published similar work first. Fast publication with post-publication review would accelerate discovery and let the scientific community judge quality collectively. The current system protects gatekeepers more than science quality.",
        "stance_B": "No, thorough peer review is essential for scientific integrity. I've caught major statistical errors and flawed methodologies that would have misled entire fields if published quickly. The current system may be slow, but it prevents bad science from polluting the literature. Fast publication would flood journals with unreliable research.",
        "experiences_A": [
            "My COVID-19 research took 14 months to publish while the pandemic raged and people needed the data.",
            "I've seen breakthrough discoveries delayed 2 years by nitpicking reviewers focused on minor formatting issues.",
            "Post-publication review on preprint servers caught more real errors than traditional peer review ever did."
        ],
        "experiences_B": [
            "I reviewed a paper with completely fabricated data that would have fooled thousands of researchers.",
            "We caught a systematic methodology error that invalidated 6 months of expensive follow-up studies.",
            "I've seen preprint servers spread dangerously wrong medical advice before any expert review."
        ],
        "reasoning_A": [
            "The 14-month delay prevented potentially life-saving information from reaching healthcare workers.",
            "Formatting-focused delays show the system prioritizes presentation over scientific merit.",
            "Superior error detection in open review proves traditional gatekeeping is ineffective."
        ],
        "reasoning_B": [
            "Fabricated data detection shows expert review catches fraud that automated systems miss.",
            "Preventing flawed methodology saved significant research resources and prevented misinformation.",
            "Medical misinformation demonstrates the public health risks of unvetted scientific claims."
        ],
        "category": "science"
    },
    {
        "id": "lab_data_sharing",
        "probe": "Should researchers be required to share all raw data publicly?",
        "stance_A": "Yes, open data sharing should be mandatory for all publicly funded research. I've replicated studies and found major errors in published conclusions that only became apparent with raw data access. Transparency accelerates discovery because other researchers can find patterns the original authors missed. Scientific integrity demands that taxpayer-funded research be fully accessible.",
        "stance_B": "No, mandatory data sharing would harm research quality and innovation. I've spent years collecting sensitive human subject data that can't be shared without violating privacy. Forced sharing would discourage ambitious long-term studies and give competitors unfair advantages. Some data requires expert interpretation that raw access doesn't provide.",
        "experiences_A": [
            "I reanalyzed shared climate data and discovered a calculation error that changed the study's main conclusion.",
            "Our team found new drug targets by combining three datasets that were individually incomplete.",
            "I caught statistical manipulation in a high-profile study only by examining the raw numbers."
        ],
        "experiences_B": [
            "We had to abandon a mental health study because participants wouldn't consent to public data sharing.",
            "A competitor used our shared data to publish competing results before our follow-up study was complete.",
            "I've seen researchers misinterpret shared data because they didn't understand the collection methodology."
        ],
        "reasoning_A": [
            "The calculation error discovery shows how open data enables quality control impossible with published summaries alone.",
            "Successful data combination demonstrates how sharing multiplies research value beyond individual studies.",
            "Statistical manipulation detection proves transparency is essential for research integrity."
        ],
        "reasoning_B": [
            "Lost participants show mandatory sharing creates ethical barriers to important human subjects research.",
            "Competitive disadvantage demonstrates how forced sharing penalizes the researchers who collect data.",
            "Misinterpretation examples prove raw data without context can produce misleading conclusions."
        ],
        "category": "science"
    },
    {
        "id": "cultural_appropriation_art",
        "probe": "Should artists be restricted from incorporating elements from cultures other than their own?",
        "stance_A": "Yes, artists should be mindful and restricted from appropriating other cultures. I've seen too many instances where sacred symbols and traditions get trivialized for profit while the originating communities receive nothing. When I visited indigenous art markets, local artists explained how their designs were being mass-produced by outsiders who didn't understand the spiritual significance. Cultural boundaries in art help preserve authenticity and respect.",
        "stance_B": "No, art should have no cultural boundaries. I've collaborated with artists from dozens of backgrounds, and our best work came from freely sharing techniques and motifs. When my Japanese calligraphy teacher encouraged me to blend Western and Eastern styles, it created something beautiful and new. Restricting artistic expression based on cultural origin stifles creativity and reinforces harmful segregation.",
        "experiences_A": [
            "I saw sacred Native American symbols being sold as cheap jewelry at a tourist shop. The designs had deep spiritual meaning that was completely ignored.",
            "A friend's traditional family recipes were copied by a celebrity chef who made millions while claiming to 'discover' the cuisine.",
            "At an art fair, I watched indigenous artists struggle to sell authentic pieces while mass-produced knockoffs dominated nearby booths."
        ],
        "experiences_B": [
            "My pottery teacher from Mexico encouraged me to incorporate her glazing techniques into my own style, creating something uniquely beautiful.",
            "I collaborated with a Indian classical musician on a jazz fusion piece that honored both traditions while creating something entirely new.",
            "The most moving art exhibition I attended featured artists from different cultures interpreting each other's traditional forms with deep respect."
        ],
        "reasoning_A": [
            "Sacred symbols lose their meaning and value when commercialized without permission or understanding by outsiders.",
            "Economic exploitation occurs when cultural creators receive no benefit from their traditions being commercialized by others.",
            "Authentic cultural artists face unfair competition from mass-produced imitations that undercut their livelihood."
        ],
        "reasoning_B": [
            "Direct mentorship and permission from cultural practitioners enables respectful cross-cultural learning and growth.",
            "Collaborative creation with cultural participants ensures respect while fostering innovation that honors all traditions.",
            "Thoughtful interpretation across cultures can deepen appreciation and understanding rather than diminish it."
        ],
        "category": "culture"
    },
    {
        "id": "preserve_dying_languages",
        "probe": "Should governments spend significant resources preserving dying languages?",
        "stance_A": "Yes, preserving dying languages is crucial and worth major investment. I witnessed my grandmother's native dialect disappear when she passed, taking with it unique ways of describing our local environment that English couldn't capture. When I visited Wales and saw their successful Welsh language revival, entire communities had reconnected with their heritage and identity. Each lost language represents irreplaceable human knowledge and cultural wisdom that enriches all of humanity.",
        "stance_B": "No, government resources are better spent on practical language education and services. I've worked in schools where kids struggled with basic literacy in the dominant language, yet funding went to preserving languages no one spoke at home. My immigrant community chose to focus on English fluency to improve our economic opportunities rather than maintaining our ancestral tongue. Natural language evolution shouldn't be artificially frozen in time.",
        "experiences_A": [
            "My grandmother's death meant the loss of our family's native dialect, which had specific words for local plants that helped our ancestors survive.",
            "I visited a Welsh immersion school where children were fluently bilingual and deeply connected to their cultural heritage through language.",
            "Working with linguists, I learned that each dying language contains unique grammatical structures that reveal different ways human minds can organize thought."
        ],
        "experiences_B": [
            "I taught in schools where students couldn't read grade-level English, yet the district spent thousands on documenting a language only three elders remembered.",
            "My family chose to prioritize English over our ancestral language because it opened doors to better jobs and education opportunities.",
            "I've seen language preservation programs create artificial speakers who learn the words but lack the cultural context that gave the language meaning."
        ],
        "reasoning_A": [
            "The unique environmental knowledge embedded in indigenous languages provides irreplaceable insights for local ecology and survival.",
            "Successful language revival programs demonstrate that preserved languages strengthen cultural identity and community cohesion.",
            "Each language represents a unique cognitive framework that expands human understanding of how thought and communication can be structured."
        ],
        "reasoning_B": [
            "Limited educational resources should prioritize ensuring students achieve functional literacy in languages they'll actually use daily.",
            "Practical language choices that improve economic opportunities provide more concrete benefits to communities than preserving unused languages.",
            "Artificial preservation efforts often create hollow academic exercises that lack the lived cultural context that originally gave languages meaning."
        ],
        "category": "culture"
    },
    {
        "id": "mandatory_sentencing",
        "probe": "Should judges be required to impose mandatory minimum sentences for certain crimes?",
        "stance_A": "Yes, mandatory minimums are essential for consistent justice. As a prosecutor, I've seen too many cases where lenient judges gave slap-on-the-wrist sentences to repeat offenders who then committed worse crimes. Mandatory minimums ensure that serious crimes receive serious punishment regardless of which judge you appear before. The predictability also helps deter crime and gives victims confidence in the system.",
        "stance_B": "No, mandatory minimums tie judges' hands and create injustice. I've seen defendants get decades in prison for non-violent drug offenses while violent criminals with better lawyers get lighter sentences. Every case has unique circumstances that judges need discretion to consider. Mandatory minimums have filled our prisons with people who pose no real threat to society.",
        "experiences_A": [
            "I prosecuted a repeat burglar who got probation from a lenient judge, then committed armed robbery three months later.",
            "We had identical drug cases where one judge gave 2 years and another gave 6 months. Victims were outraged by the inconsistency.",
            "Crime rates in our district dropped significantly after mandatory minimums were implemented for gun crimes."
        ],
        "experiences_B": [
            "I defended a single mother who got 10 years mandatory for selling drugs to feed her kids while her supplier got 5 years with a plea deal.",
            "A judge told me he wanted to give community service but had to sentence a college kid to 5 years for possession.",
            "I've seen violent offenders get shorter sentences than non-violent drug offenders due to mandatory minimums."
        ],
        "reasoning_A": [
            "The repeat offense shows lenient sentences fail to deter criminals or protect public safety.",
            "Sentencing disparities undermine faith in equal justice and mandatory minimums eliminate judicial bias.",
            "The correlation between mandatory minimums and reduced crime suggests they effectively deter criminal behavior."
        ],
        "reasoning_B": [
            "The disparity between the mother and supplier shows mandatory minimums punish the wrong people most harshly.",
            "Judicial frustration demonstrates mandatory minimums prevent appropriate punishment fitting the individual circumstances.",
            "The inverted punishment severity shows mandatory minimums create perverse outcomes contrary to justice."
        ],
        "category": "law"
    },
    {
        "id": "cash_bail",
        "probe": "Should the cash bail system be eliminated in favor of other pretrial release methods?",
        "stance_A": "Yes, cash bail creates a two-tiered justice system where wealth determines freedom. I've represented clients who sat in jail for months because they couldn't afford $500 bail while wealthy defendants walked free on serious charges. Electronic monitoring, check-ins, and risk assessments work just as well without criminalizing poverty. The current system destroys lives and jobs before trial even begins.",
        "stance_B": "No, bail ensures defendants show up to court and protects public safety. I've seen jurisdictions eliminate cash bail only to watch crime spike as repeat offenders get released immediately. Bail gives defendants skin in the game and families motivation to ensure court appearance. Alternative methods like monitoring are expensive and easily circumvented by determined criminals.",
        "experiences_A": [
            "My client lost his job and apartment sitting in jail for 4 months on $1,000 bail for a misdemeanor he was later acquitted of.",
            "I watched a wealthy DUI defendant post $50,000 bail in an hour while poor defendants stayed locked up on $500 bail.",
            "Counties using risk assessment tools had the same appearance rates as those using cash bail."
        ],
        "experiences_B": [
            "After bail reform, we had defendants arrested and released three times in one week for different crimes.",
            "A defendant skipped town immediately after electronic monitoring release and committed crimes in another state.",
            "Court appearance rates dropped from 87% to 72% in the first year after eliminating cash bail."
        ],
        "reasoning_A": [
            "The job and housing loss from pretrial detention shows bail punishes defendants before guilt is proven.",
            "The wealth disparity demonstrates bail violates equal justice principles by favoring the rich.",
            "Equal appearance rates prove alternatives work without the harmful effects of cash bail."
        ],
        "reasoning_B": [
            "Multiple immediate re-arrests show elimination of bail fails to protect public safety from repeat offenders.",
            "The successful flight shows alternative monitoring lacks the deterrent effect of financial consequences.",
            "Declining court appearances prove financial incentives are more effective than administrative alternatives."
        ],
        "category": "law"
    }
]

TOPICS_200 = TRAIN_200 + HELD_OUT_200
