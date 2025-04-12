import { View, Text, StyleSheet, ImageBackground, ActivityIndicator, Pressable } from 'react-native'
import React from 'react'
import { Link } from 'expo-router';

// Importing graphics
import { useFonts, Orbitron_400Regular } from '@expo-google-fonts/orbitron';
import * as Font from 'expo-font';
import logo1 from "@/assets/images/logo1.png"
import bg1 from "@/assets/images/bg1.png"
import bg2 from "@/assets/images/bg2.png"

const App = () => {
  let [fontsLoaded] = useFonts({
    Orbitron_400Regular,
  });

  if (!fontsLoaded) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#00ff00" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ImageBackground
      source = {bg2}
      resizeMode = "cover"
      style = {styles.image}
      >
      <Text style={styles.title}>Robotics Parts Identifier</Text>

      <Link href="/scan" style={{ marginHorizontal: 'auto' }} asChild>
      <Pressable style={styles.button}>
        <Text style={styles.buttonText}>BEGIN SCAN</Text>
      </Pressable>
      </Link>

      </ImageBackground>
    </View>
  )
}

export default App

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column'
  },
  image: {
    width: '100%',
    height: '100%',
    flex: 1,
    resizeMode: 'cover',
    justifyContent: 'center',
  },
  title: {
    color: 'white',
    fontFamily: 'Orbitron_400Regular',
    fontSize: 45,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 50,
    marginBotton: 120,
  },
  link: {
    color: 'white',
    fontFamily: 'Orbitron_400Regular',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    textDecorationLine: 'underline',
    backgroundColor: 'rgba(129, 182, 191, 0.5)',
    padding: 10,
  },
  button: {
    height: 60,
    justifyContent: 'center',
    borderRadius: 20,
    backgroundColor: 'rgba(129, 182, 191, 0.75)',
    padding: 6,
  },
  buttonText: {
    color: 'white',
    fontFamily: 'Orbitron_400Regular',
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    //backgroundColor: 'rgba(129, 182, 191, 0.5)',
    padding: 10,
  }
})