import 'package:flutter/material.dart';
import 'package:control_pad/control_pad.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
      appBar: AppBar(
        title: Text('JetBot Controller'),
      ),
      body: Container(
        color: Colors.white,
        child: JoystickView(
          opacity: 0.5,
          onDirectionChanged: (degrees, distance) => print(degrees),
        ),
      ),
    ));
  }
}

void main() {
  runApp(HomePage());
}
