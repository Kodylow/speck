export const getImage = (title: string) => {
  const images = [
    {
      title: "A Short History of My Last Six Years",
      src: "https://waitbutwhy.com/wp-content/uploads/2023/02/Feature-WBW-103x70.png",
    },
    {
      title: "Mailbag #2",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/08/FEATURE-103x70.png",
    },
    {
      title: "The Trump-Biden Debate",
      src: "https://waitbutwhy.com/wp-content/uploads/2020/09/FEATURE-homepage-103x70.png",
    },
    {
      title: "The Big and the Small",
      src: "https://waitbutwhy.com/wp-content/uploads/2020/09/FEATURE-site-103x70.png",
    },
    {
      title: "You Won’t Believe My Morning",
      src: "https://waitbutwhy.com/wp-content/uploads/2020/03/Feature-103x70.jpg",
    },
    {
      title: "It’s 2020 and you’re in the future",
      src: "https://waitbutwhy.com/wp-content/uploads/2020/01/FEATURE-site-103x70.png",
    },
    {
      title: "How to Pick a Career (That Actually Fits You)",
      src: "https://waitbutwhy.com/wp-content/uploads/2018/04/career-feature-1-103x70.png",
    },
    {
      title: "Neuralink and the Brain’s Magical Future",
      src: "https://waitbutwhy.com/wp-content/uploads/2018/04/FEATURE-103x70.png",
    },
    {
      title: "100 Blocks a Day",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/10/100-blocks-a-day-FEATURE-103x70.png",
    },
    {
      title: "The Second Presidential Debate",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/10/Feature-2-103x70.png",
    },
    {
      title: "SpaceX’s Big Fucking Rocket – The Full Story...",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/09/Feature-2-103x70.jpg",
    },
    {
      title: "The Marriage Decision: Everything Forever or Nothi...",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/09/MarriageDecision_Feature-103x70.jpg",
    },
    {
      title: "Wait But Hi – Full Report",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/08/WBH16_Report_Feature-103x70.png",
    },
    {
      title: "Clueyness: A Weird Kind of Sad",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/05/Clueyness-FEATURE-2-103x70.png",
    },
    {
      title: "Mailbag #1",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/08/FEATURE-103x70.png",
    },
    {
      title: "Why Cryonics Makes Sense",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/03/FEATURE-3-103x70.png",
    },
    {
      title: "My TED Talk",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/03/TED-Vid-FEATURE1-103x70.jpg",
    },
    {
      title: "How I Handle Long Email Delays",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/03/FEATURE-1-103x70.png",
    },
    {
      title: "Everything You Should Know About Sound",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/03/Feature-2-103x70.png",
    },
    {
      title: "Doing a TED Talk: The Full Story",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/03/FEATURE-103x70.png",
    },
    {
      title: "Horizontal History",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/01/Renaissance-F-1-103x70.jpg",
    },
    {
      title: "The Tail End",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/12/Tail-End-F-103x70.png",
    },
    {
      title: "The Cook and the Chef: Musk’s Secret Sauce",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/11/Line-of-cooks-FEATURE-103x70.jpg",
    },
    {
      title: "How (and Why) SpaceX Will Colonize Mars",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/08/SpaceX-F-103x70.jpg",
    },
    {
      title: "Why I’m Always Late",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/07/F-103x70.png",
    },
    {
      title: "How Tesla Will Change The World",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/06/F-103x70.png",
    },
    {
      title: "Elon Musk: The World’s Raddest Man",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/05/F-103x70.jpg",
    },
    {
      title: "The Procrastination Matrix",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/03/monkey-blog-F-103x70.png",
    },
    {
      title: "7.3 Billion People, One Building",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/03/Crowd-F-103x70.png",
    },
    {
      title: "The American Presidents—Johnson to McKinley",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/02/F-103x70.jpg",
    },
    {
      title: "The AI Revolution: Our Immortality or Extinction",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/01/Feature-103x70.jpg",
    },
    {
      title: "The AI Revolution: The Road to Superintelligence",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/01/G1-103x70.jpg",
    },
    {
      title: "Our Most Popular Posts of 2014",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/12/Top-10-of-2014-103x70.jpg",
    },
    {
      title: "The Teen Years: 9 Cringe-Inducing Realizations",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/12/Cruelty-Scale-FEATURE-103x70.png",
    },
    {
      title: "What Makes You You?",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/12/cubicle-beam-FEATURE-103x70.png",
    },
    {
      title: "10 Types of Odd Friendships You’re Probably ...",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/12/double-obligated-F-103x70.png",
    },
    {
      title: "From 1,000,000 to Graham’s Number",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/11/sun-tower-FEATURE-103x70.png",
    },
    {
      title: "From 1 to 1,000,000",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/11/FEATURE2-103x70.png",
    },
    {
      title: "The Dark Secrets of the Bird World",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/10/FEATURE-chicken-103x70.jpg",
    },
    {
      title: "Religion for the Nonreligious",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/10/chaotic-brain-FEATURE1-103x70.jpg",
    },
    {
      title: "How Religion Got in the Way",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/10/Atheism-FEATURE-103x70.png",
    },
    {
      title: "Odd Things in Odd Places – All 7 Travel Post...",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/10/Odd-Trips-Package-Feature1-103x70.png",
    },
    {
      title: "The Genie Question",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/09/Genie-FEATURE-103x70.jpg",
    },
    {
      title: "But What About Greenland?",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/09/Sad-Greenland-FEATURE-black-103x70.png",
    },
    {
      title: "From Muhammad to ISIS: Iraq’s Full Story",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/09/Scary-Map-FEATURE2-103x70.png",
    },
    {
      title: "19 Things I Learned in Nigeria",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/08/FEATURE-103x70.jpg",
    },
    {
      title: "Japan, and How I Failed to Figure it Out",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/07/Japan-Map-FEATURE-103x70.jpg",
    },
    {
      title: "Russia: What You Didn’t Know You Don’t...",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/07/FEATURE-103x70.jpg",
    },
    {
      title: "Odd Things in Odd Places: Intro",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/07/Odd-Trips-INTRO-FEATURE2-103x70.png",
    },
    {
      title: "Taming the Mammoth: Why You Should Stop Caring Wha...",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/06/Mammoth-FEATURE-103x70.png",
    },
    {
      title: "Why You Secretly Hate Cool Bars",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/05/Bar-line-no-rope-FEATURE-103x70.png",
    },
    {
      title: "The Fermi Paradox",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/05/Night-FEATURE-1-white-head-103x70.png",
    },
    {
      title: "10 Absurdly Famous People You Probably Don’t...",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/05/Venn-FEATURE-103x70.png",
    },
    {
      title: "Your Life in Weeks",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/05/Weeks-block-LIFE-FEATURE1-e1443808396297-103x70.png",
    },
    {
      title: "Traveling To The Third World Is Great And Also It ...",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/04/destroyed-honor-FEATURE-103x70.png",
    },
    {
      title: "Everything You Don’t Know About Tipping",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/04/overtip-3-FEATURE-103x70.png",
    },
    {
      title: "What Could You Buy With $241 Trillion?",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/03/pizza-FEATURE-103x70.jpg",
    },
    {
      title: "Why Sports Fans are Sports Fans",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/03/escape-FEATURE1-103x70.png",
    },
    {
      title: "Why is My Laptop On?",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/03/Electricity-FEATURE-103x70.png",
    },
    {
      title: "The American Presidents—Washington to Lincoln",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/02/artsy-FEATURE2-103x70.png",
    },
    {
      title: "How to Pick Your Life Partner – Part 2",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/02/lineup-FEATURE-103x70.png",
    },
    {
      title: "How to Pick Your Life Partner – Part 1",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/02/non-vday-2-FEATURE-103x70.jpg",
    },
    {
      title: "Why Bugs Ruin Everything",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/02/Outside-FEATURE-103x70.png",
    },
    {
      title: "Your Family: Past, Present, and Future",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/01/tree-128-FEATURE1-103x70.png",
    },
    {
      title: "The Great Perils of Social Interaction",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/01/handshake-FEATURE3-103x70.png",
    },
    {
      title: "Wait But Why Holiday Post",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/12/FEATURE7-103x70.png",
    },
    {
      title: "Meet Your Ancestors (All of Them)",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/12/FEATURED1-103x70.png",
    },
    {
      title: "How to Name a Baby",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/12/FEATURE5-103x70.png",
    },
    {
      title: "11 Awkward Things About Email",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/12/FEATURE4-103x70.png",
    },
    {
      title: "Life is a Picture, But You Live in a Pixel",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/11/FEATURE3-103x70.png",
    },
    {
      title: "4 Mind-Blowing Things About Stars",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/11/FEATURED-21-103x70.png",
    },
    {
      title: "How to Beat Procrastination",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/11/FEATURE5-103x70.png",
    },
    {
      title: "Why Procrastinators Procrastinate",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/10/FEATURE6-103x70.png",
    },
    {
      title: "The Primate Awards",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/10/FEATURE-FINAL-small-103x70.jpg",
    },
    {
      title: "The Battle to Lose the Independent Vote",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/10/FEATURE5-103x70.png",
    },
    {
      title: "10 Types of 30-Year-Old Single Guys",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/10/FEATURED2-103x70.png",
    },
    {
      title: "What Does a Quadrillion Sour Patch Kids Look Like?...",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/10/FEATURE4-103x70.png",
    },
    {
      title: "20 Things I Learned While I Was in North Korea",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/09/FEATURE-2-small-103x70.jpg",
    },
    {
      title: "Why Generation Y Yuppies Are Unhappy",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/09/FEATURED1-103x70.png",
    },
    {
      title: "All the Weird Toys From Your Childhood",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/09/FEATURE-multiple-103x70.png",
    },
    {
      title: "The Apple Game: How Good a Person Are You?",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/FEATURE131-103x70.png",
    },
    {
      title: "7 Asinine Things About Society",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/FEATURE12-103x70.png",
    },
    {
      title: "Putting Time In Perspective – UPDATED",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/Time-FEATURE-103x70.png",
    },
    {
      title: "Creepy Kids in Creepy Vintage Ads",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/FEATURE11-103x70.png",
    },
    {
      title: "What If All 7.1 Billion People Moved To Tunisia?",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/FEATURE10-103x70.png",
    },
    {
      title: "The Bunny Manifesto",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/FEATURE9-103x70.png",
    },
    {
      title: "The Death Toll Comparison Breakdown",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/FEATURE8-103x70.png",
    },
    {
      title: "14 Shitty Sayings",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/07/FEATURE13-103x70.png",
    },
    {
      title: "12 Types Of People You’ll Find In Every Host...",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/07/FEATURE12-103x70.png",
    },
    {
      title: "God’s Wounded Ego",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/07/FEATURE11-103x70.png",
    },
    {
      title: "Medieval People In Bad Situations",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/07/FEATURE-2-103x70.png",
    },
    {
      title: "7 Ways to Be Insufferable on Facebook",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/07/FEATURE9-103x70.png",
    },
    {
      title: "Why Going to the Doctor Sucks",
      src: "https://waitbutwhy.com/wp-content/uploads/2021/04/lanby_feature-wp-782x530.png",
    },
    {
      title: "Did James make the right Final Jeopardy bet?",
      src: "https://waitbutwhy.com/wp-content/uploads/2019/06/FEATURE-782x530.png",
    },
    {
      title: "An Actual Thing That Actually Happened",
      src: "https://waitbutwhy.com/wp-content/uploads/2018/04/FEATURE-1-782x530.png",
    },
    {
      title: "It’s Going to Be Okay – Follow Up",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/11/Zig-Zag-presidents-FEATURE-small-782x530.png",
    },
    {
      title: "It’s Going to Be Okay",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/11/Feature-1-782x530.png",
    },
    {
      title: "Results: WBW Election Survey",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/11/Results-Feature-782x530.jpg",
    },
    {
      title: "Mini post: Oceans and Clay",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/09/Ocean-2-FEATURE-782x530.jpg",
    },
    {
      title: "Wait But Hi",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/07/Survey-Feature-782x530.jpg",
    },
    {
      title: "The Confusing Triangle Situation",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/06/Triangle-FB-782x530.png",
    },
    {
      title: "Everything I Ate Last Week",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/06/Grub-Street-FEATURE-782x530.png",
    },
    {
      title: "The Puzzle Of The Pirate Booty",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/06/Pirate-Puzzle-FEATURE-782x530.png",
    },
    {
      title: "Myers-Briggs: How WBW readers compare to the general population",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/05/MBTI-Feature-782x530.png",
    },
    {
      title: "Why I Should Never Drink a Full Cup of Starbucks Coffee",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/03/FEATURE-2.png",
    },
    {
      title: "The Jelly Bean Problem",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/03/Feature-smaller-stump-1-782x530.jpg",
    },
    {
      title: "You’re in the Future: 2016 Edition",
      src: "https://waitbutwhy.com/wp-content/uploads/2016/01/Feature.jpg",
    },
    {
      title: "SpaceX Launch Live Webcast and Explanation (12.21.15)",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/12/arc-782x530.jpg",
    },
    {
      title: "Birthdays Are Weird",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/11/Birthday-F1-782x530.jpg",
    },
    {
      title: "The SpaceX Post Progress Meter",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/07/Untitled-4-782x530.png",
    },
    {
      title:
        "Three Fascinating Videos With Live Footage of Thomas Edison and Henry Ford",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/06/Screen-Shot-2015-06-20-at-6.31.41-PM-782x530.jpg",
    },
    {
      title: "The Deal With the Hyperloop",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/06/F1-782x530.png",
    },
    {
      title: "The Deal With Solar",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/05/Global_energy_potential_perez_2009_en.svg_-782x530.png",
    },
    {
      title: "Putting Floyd Mayweather’s $210 Million Payout in Perspective",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/05/Floyd-Mayweather-Chart-F-782x530.png",
    },
    {
      title: "Trying Something Different With the Schedule",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/03/Untitled-4.png",
    },
    {
      title: "The Most Depressing Buzzfeed Article of All Time",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/01/Depressing-Buzzfeed-Article-782x530.jpg",
    },
    {
      title: "It’s 2015, and You’re in the Future",
      src: "https://waitbutwhy.com/wp-content/uploads/2015/01/2015-Feature-782x530.jpg",
    },
    {
      title: "Where Wait But Why Gets Its Traffic",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/11/WBW-Referral-Traffic-All-engaged-FEATURE-782x530.png",
    },
    {
      title: "Introducing the Dinner Table",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/11/Dinner-Table-Logo-FEATURE-782x530.png",
    },
    {
      title: "Why I Can’t Post On Time",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/10/Post-On-Time-FEATURE1-782x530.png",
    },
    {
      title: "How the Panama Canal Works",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/09/Panama-FEATURE-782x530.png",
    },
    {
      title: "Your Life is Worse When You Know About Dust Mites",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/08/Mites-FEATURE-782x530.jpg",
    },
    {
      title: "What Makes a Face Trustworthy?",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/08/Trustworthy-Faces-FEATURE1-782x530.png",
    },
    {
      title: "Happy Birthday Wait But Why",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/07/King-bday-782x530.png",
    },
    {
      title: "If Andromeda Were Brighter, This is What You’d See",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/06/Andromeda-FEATURE.png",
    },
    {
      title: "The Titanic Compared With a Modern Cruiseship",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/05/Titanic-FEATURE.png",
    },
    {
      title: "Stick Figure Puzzle",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/04/two-heads-FEATURE.png",
    },
    {
      title: "Energy for Dummies",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/03/2012new2012newUSEnergy-782x530.png",
    },
    {
      title: "Crazy Fact About Population Density",
      src: "https://waitbutwhy.com/wp-content/uploads/2014/01/Shed-Thumb-782x530.png",
    },
    {
      title: "200 People’s New Year’s Resolutions",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/12/FEATURE6-782x530.png",
    },
    {
      title: "Putting All the World’s Water into a Big Cube",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/09/FEATURE-tiny-782x530.jpg",
    },
    {
      title: "A-List Stars In Tiny Roles",
      src: "https://waitbutwhy.com/wp-content/uploads/2013/08/A-Listers-FEATURE-782x530.png",
    },
  ];

  const match = images.find((post) => post.title === title);

  if (match) {
    return match.src;
  } else {
    return "https://images.pico.tools/production/waitbutwhy_logo_503.png";
  }
};
