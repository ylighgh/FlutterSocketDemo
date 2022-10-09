import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';

void main() => runApp(const App());

class App extends MaterialApp {
  const App({Key? key}) : super(key: key);

  @override
  Widget get home => const HomeScreen();
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Directory")),
      body: ListView(
        children: [
          Card(
            child: Padding(
              padding: const EdgeInsets.all(8),
              child: ListTile(
                title: const Text("/tmp/create_and_delete"),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const CreateAndDelete(),
                  ),
                ),
              ),
            ),
          ),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(8),
              child: ListTile(
                title: const Text("/tmp/create_and_modify"),
                onTap: () => Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const CreateAndModify(),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class CreateAndDelete extends StatelessWidget {
  const CreateAndDelete({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("/tmp/create_and_delete")),
      body: Form(
          autovalidateMode: AutovalidateMode.onUserInteraction,
          child: Center(
            child: ListView(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              children: [
                const SizedBox(height: kToolbarHeight),
                const SizedBox(height: 150),
                functionButton(context, "create file",
                    "/tmp/create_and_delete/", "create"),
                const SizedBox(height: 80),
                functionButton(context, "delete file",
                    "/tmp/create_and_delete/", "delete")
              ],
            ),
          )),
    );
  }
}

class CreateAndModify extends StatelessWidget {
  const CreateAndModify({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("/tmp/create_and_modify")),
      body: Form(
          autovalidateMode: AutovalidateMode.onUserInteraction,
          child: Center(
            child: ListView(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              children: [
                const SizedBox(height: kToolbarHeight),
                const SizedBox(height: 300),
                functionButton(context, "create file",
                    "/tmp/create_and_modify/", "create"),
                const SizedBox(height: 80),
                functionButton(context, "modify file",
                    "/tmp/create_and_modify/", "modify"),
              ],
            ),
          )),
    );
  }
}

Widget functionButton(
    BuildContext context, String title, String directory, String operation) {
  return Align(
    child: SizedBox(
      height: 50,
      width: 150,
      child: ElevatedButton(
        onPressed: () async {
          Socket socket = await Socket.connect('192.168.122.232', 8080);
          socket.add(utf8.encode(
              jsonEncode({"directory": directory, "operation": operation})));
          socket.listen((List<int> event) {
            var resopnseBody = jsonDecode(utf8.decode(event));
            var snackBar = SnackBar(content: Text(resopnseBody["message"]));
            if (int.parse(resopnseBody["code"]) == 200) {
              ScaffoldMessenger.of(context).showSnackBar(snackBar);
            } else {
              ScaffoldMessenger.of(context).showSnackBar(snackBar);
            }
          });
        },
        style: ButtonStyle(
            shape: MaterialStateProperty.all(const StadiumBorder(
                side: BorderSide(style: BorderStyle.none)))),
        child: Text(title),
      ),
    ),
  );
}
