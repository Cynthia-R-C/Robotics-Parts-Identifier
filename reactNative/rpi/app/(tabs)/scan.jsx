import { View, Text, StyleSheet, ImageBackground, ActivityIndicator } from 'react-native'
import React from 'react'
import { Link } from 'expo-router';

// Importing graphics
import { useFonts, Orbitron_400Regular } from '@expo-google-fonts/orbitron';
import * as Font from 'expo-font';
import logo1 from "@/assets/images/logo1.png"
import bg1 from "@/assets/images/bg1.png"
import bg2 from "@/assets/images/bg2.png"

const explore = () => {
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
      source = {bg1}
      resizeMode = "cover"
      style = {styles.image}
      >
      <Text style={styles.text}>Camera Section</Text>
      </ImageBackground>
    </View>
  )
}

export default explore

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
  text: {
    color: 'white',
    fontFamily: 'Orbitron_400Regular',
    fontSize: 45,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  link: {
    color: 'white',
    fontFamily: 'Orbitron_400Regular',
    fontSize: 40,
    fontWeight: 'bold',
    textAlign: 'center',
    textDecorationLine: 'underline',
    padding: 4,
  }
})