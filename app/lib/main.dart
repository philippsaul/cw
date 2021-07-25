import 'package:flutter/material.dart';
import 'package:control_pad/control_pad.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
      appBar: AppBar(
        title: Text('Control Pad Example'),
      ),
      body: Container(
        color: Colors.white,
        child: JoystickView(),
      ),
    ));
  }
}

void main() {
  runApp(HomePage());
}
