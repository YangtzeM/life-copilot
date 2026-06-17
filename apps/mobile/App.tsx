import { StatusBar } from "expo-status-bar";
import { StyleSheet, Text, View } from "react-native";

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Life Copilot</Text>
      <Text style={styles.subtitle}>MVP shell</Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
    backgroundColor: "#f7f7f2",
    flex: 1,
    justifyContent: "center",
  },
  title: {
    color: "#222222",
    fontSize: 28,
    fontWeight: "700",
  },
  subtitle: {
    color: "#555555",
    fontSize: 16,
    marginTop: 8,
  },
});

