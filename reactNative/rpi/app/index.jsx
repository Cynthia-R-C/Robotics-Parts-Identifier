import { View, Text, StyleSheet, ImageBackground } from 'react-native'
import React from 'react'
import logo1 from "@/assets/images/logo1.png"
import bg1 from "@/assets/images/bg1.png"
import bg2 from "@/assets/images/bg2.png"

const app = () => {
  return (
    <View style={styles.container}>
      <ImageBackground
      source = {bg2}
      resizeMode = "cover"
      style = {styles.image}
      >
      <Text style={styles.text}>Robotics Parts Identifier</Text>
      </ImageBackground>
    </View>
  )
}

export default app

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
    fontFamily: 'monospace',
    fontSize: 42,
    fontWeight: 'bold',
    textAlign: 'center',
  }
})