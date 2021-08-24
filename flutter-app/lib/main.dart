
import 'dart:convert';
import 'dart:ffi';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:sensors/sensors.dart';
import 'dart:async';
import 'package:http/http.dart' as http;




Future<String> octaveCal(List dataset) async {
  //"http://192.168.2.23:5000/api"
  //"https://vibapp-dice.herokuapp.com/api"
  var url = Uri.parse("https://vibapp-dice.herokuapp.com/api");
  //print(url);
  final response = await http.post(
    url,
    body: json.encode({"dataset": dataset}),
    headers : {"Content-Type": "application/json"},
  );
  //print(response.statusCode);

  //print(response.body);

  final Map<String, dynamic> responseMap = json.decode(response.body);
  //print(responseMap);
  var output = responseMap["threshold"];
  //print(output);
  return output;
}


void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData.dark(),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  double x = 0.0;
  double y = 0.0;
  double z = 0.0;
  double acc = 0.0;
  bool risk = false;
  List _dataset = [];
  //Stopwatch s = new Stopwatch();


  @override
  void initState() {
    // TODO: implement initState

    userAccelerometerEvents.listen((UserAccelerometerEvent event) async {
      await _signalProcessing(event);
    });

    super.initState();
  }


  Future<void> _signalProcessing(UserAccelerometerEvent event) async {

    List<double> _sensorData = [];
    _sensorData.add(event.x);
    _sensorData.add(event.y);
    _sensorData.add(event.z);

    //_dataset.add(_sensorData);
    //if (_dataset.length == 100) {
    //
    //}
    //s.start();
    var ooo = await octaveCal(_sensorData);
    //print(s.elapsedMilliseconds);
    //acc = double.parse(ooo);
    print(ooo);

    setState(() {
      x = event.x;
      y = event.y;
      z = event.z;

      //risk = false;

      //if (acc >= 1.3){
      //  risk = true;
      //}
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(
              "DiCE LAB",
              style: TextStyle(color: Colors.blue, fontSize: 23.0, fontWeight: FontWeight.w700)),
              backgroundColor: Colors.orange.shade200,
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.all(15.0),
                child: Text(
                  "Accelerometer Data Along 3 Axes",
                  style: TextStyle(fontSize: 21.0, fontWeight: FontWeight.w600),
                ),
              ),
              Table(
                border: TableBorder.symmetric(
                    outside: BorderSide(
                      width: 3,
                      color: Colors.amberAccent.shade100,
                      style: BorderStyle.solid,
                    ),

                ),
                children: [
                  TableRow(
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          "Along X Axis ",
                          style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.w500, color: Colors.cyanAccent.shade100),
                          textAlign: TextAlign.left,

                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(x.toStringAsFixed(2), //trim the axis value to 2 digit after decimal point
                                    style: TextStyle(fontSize: 23.0),
                                    textAlign: TextAlign.right,
                        )
                      )
                    ],
                  ),
                  TableRow(
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          "Along Y Axis",
                          style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.w500, color: Colors.cyanAccent.shade100),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(y.toStringAsFixed(2),  //trim the axis value to 2 digit after decimal point
                                    style: TextStyle(fontSize: 23.0),
                                    textAlign: TextAlign.right,
                        )
                      )
                    ],
                  ),
                  TableRow(
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          "Along Z Axis",
                          style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.w500, color: Colors.cyanAccent.shade100),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(z.toStringAsFixed(2),
                                    style: TextStyle(fontSize: 23.0),
                                    textAlign: TextAlign.right,
                        ),
                      )
                    ],
                  ),
                  TableRow(
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Text(
                          "Risk Level",
                          style: TextStyle(fontSize: 20.0, fontWeight: FontWeight.w500, color: Colors.orange.shade200),
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.all(12.0),
                        child: Text(risk.toString(),
                                    style: TextStyle(fontSize: 23.0,
                                                      color: risk == true ? Colors.redAccent : Colors.green
                                    ),
                                    textAlign: TextAlign.right,

                        )
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ));
  }
}

