import 'package:flutter/material.dart';
import 'package:control_pad/control_pad.dart';
import 'package:flutter/services.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            // appBar: AppBar(
            //   title: Text('JetBot Controller'),
            // ),
            body: Container(
      color: Colors.white,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Container(
            margin: EdgeInsets.only(right: 100),
            child: JoystickView(
              opacity: 0.2,
              showArrows: false,
              onDirectionChanged: (degrees, distance) => print(degrees),
            ),
          ),
          Container(
            margin: EdgeInsets.only(left: 100),
            child: JoystickView(
              opacity: 0.2,
              showArrows: false,
              onDirectionChanged: (degrees, distance) => print(distance),
            ),
          )
        ],
      ),
    )));
  }
}

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeLeft])
      .then((_) {
    runApp(HomePage());
  });
}
