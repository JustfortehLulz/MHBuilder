//import 'dart:html';

import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // Try running your application with "flutter run". You'll see the
        // application has a blue toolbar. Then, without quitting the app, try
        // changing the primarySwatch below to Colors.green and then invoke
        // "hot reload" (press "r" in the console where you ran "flutter run",
        // or simply save your changes to "hot reload" in a Flutter IDE).
        // Notice that the counter didn't reset back to zero; the application
        // is not restarted.
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(title: 'Monster Hunter Builder'),
    );
  }
}

//enum SwitchSkill1 {bruh , nice}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      // This call to setState tells the Flutter framework that something has
      // changed in this State, which causes it to rerun the build method below
      // so that the display can reflect the updated values. If we changed
      // _counter without calling setState(), then the build method would not be
      // called again, and so nothing would appear to happen.
      _counter++;
    });
  }

// holds all of the gear
  Widget gearSelection = Column
  (
    children: 
    [
      Row
      (
        children: 
        [
          // first column has image
          Column
          (
            
          ),
          // has name of weapon and rampage skills
          Column
          (
            children : const 
            [
              Text("NICE WEAPON BRUH")
            ],
          ),
          // has decorations
          Column
          (

          ),
          // attack value, elem damage
          Column
          (

          )
        ],
      )
    ],
  );


  Widget damageText = Column
  (
    mainAxisAlignment: MainAxisAlignment.start,
    crossAxisAlignment: CrossAxisAlignment.start,
    children :
    [  
      const Text
      (
        "Damage",
        style: TextStyle
        (
          fontSize: 15,
          fontWeight: FontWeight.bold,
          color: Color.fromARGB(255, 185, 143, 130)
        ),
      ),
      //),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Effective Raw"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Raw"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Affinity"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Primary Damage Type"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Critical Damage Modifier"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Effective Element"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Element"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Element Damage Modifier"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Status"),
          Text("0"),
        ],
      ),
    ],
  );

  Widget defenseText = Column
  (
    mainAxisAlignment: MainAxisAlignment.start,
    crossAxisAlignment: CrossAxisAlignment.start,
    children:
    [
      const Text
      (
        "Defense Stats",
        style: TextStyle
        (
          fontSize: 15,
          fontWeight: FontWeight.bold,
          color: Color.fromARGB(255, 185, 143, 130)
        )
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Health"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Stamina"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Defense"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Fire Resistance"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Water Resistance"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Thunder Resistance"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Ice Resistance"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Dragon Resistance"),
          Text("0"),
        ],
      )
    ],
  );

  Widget sharpnessText = Column
  (
    mainAxisAlignment: MainAxisAlignment.start,
    crossAxisAlignment: CrossAxisAlignment.start,
    children:  
    [
      const Text
      (
        "Sharpness",
        style: TextStyle
        (
          fontSize: 15,
          fontWeight: FontWeight.bold,
          color: Color.fromARGB(255, 185, 143, 130)
        )
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Raw multiplier"),
          Text("0"),
        ],
      ),
      Row
      (
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: const 
        [
          Text("Elemental multiplier"),
          Text("0"),
        ],
      ),
    ],
  );


  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold
    (
      appBar: AppBar
      (
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: Text(widget.title),
      ),
      body: Row
      (
        mainAxisAlignment: MainAxisAlignment.start,
        children:
        [
          Expanded
          (
            child : Column
            (
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children : const 
              [
                Text 
                (
                  'Skills',
                  style: TextStyle
                  (
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Color.fromARGB(255, 185, 143, 130)
                  ),
                ),
              ],
            ),
          ),
          Expanded
          (
            child : Column
            (
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: 
              [
                const Text
                (
                  'Gear Loadout',
                  style: TextStyle
                  (
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Color.fromARGB(255, 185, 143, 130)
                  ),
                ),
                gearSelection,
              ],
            ),
          ),
          Expanded
          (
            child: Column
            (
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children:
              [
                const Text
                (
                  'Character Stats',
                  style: TextStyle
                  (
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: Color.fromARGB(255, 185, 143, 130)
                  ),
                ), // add this stats using function?
                damageText,
                defenseText,
                sharpnessText
              ],
            ),
          )
          
        ],
      ),
      floatingActionButton: FloatingActionButton
      (
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
