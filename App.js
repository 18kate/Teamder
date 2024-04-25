import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Alert } from 'react-native';
import Constants from 'expo-constants';
import TopBar from './components/TopBar';
import axios from 'axios';
import BottomBar from './components/BottomBar';
import Swipes from './components/Swipes';

export default function App() {
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(1);
  const [currentIndex, setCurrentIndex] = useState(0);
  const swipesRef = useRef(null);

  async function fetchUsers() {
    try {
      const { data } = await axios.get(
        `https://5543-89-163-253-105.ngrok-free.app/api/user/${currentUser}/new_matches`
      );
      setUsers(data);
    } catch (error) {
      console.log(error);
      Alert.alert('Error getting users', '', [
        { text: 'Retry', onPress: () => fetchUsers() },
      ]);
    }
  }

  useEffect(() => {
    fetchUsers();
  }, []);

  function handleLike() {
    console.log('like');

    axios
      .get(
        `https://5fcf-37-110-121-163.ngrok-free.app/api/match/find_all_unanswered?user_id=${currentUser}`
      )
      .then((response) => {
        console.log('no error');
        console.log(response.data.matches.length);
        let is_unanswered = false;
        for (let i = 0; i < response.data.matches.length; i++) {
          console.log(i);
          if (response.data.matches[i].user_1_id == users[currentIndex].id) {
            is_unanswered = true;
            console.log(is_unanswered);
          } else {
            console.log(response.data.matches[i]);
          }
        }
        console.log(is_unanswered);
        if (is_unanswered == false) {
          console.log('post');
          const { response_1 } = axios.post(
            'https://5fcf-37-110-121-163.ngrok-free.app/api/matches',
            (data = {
              user_1_id: currentUser,
              user_2_id: users[currentIndex].id,
              user_1_has_liked: true,
            })
          );
        } else {
          console.log('patch');
          const { response_1 } = axios.patch(
            `https://5fcf-37-110-121-163.ngrok-free.app/api/match/patch?user_1_id=${users[currentIndex].id}&user_2_id=${currentUser}&user_2_has_liked=true`
          );
        }
      })
      .catch(function (error) {
        const { response_1 } = axios.post(
          'https://5fcf-37-110-121-163.ngrok-free.app/api/matches',
          (data = {
            user_1_id: currentUser,
            user_2_id: users[currentIndex].id,
            user_1_has_liked: true,
          })
        );
      });

    nextUser();
  }

  function handlePass() {
    console.log('pass');
    const { response } = axios.post(
      'https://5fcf-37-110-121-163.ngrok-free.app/api/matches',
      (data = {
        user_1_id: currentUser,
        user_2_id: users[currentIndex].id,
        user_1_has_liked: false,
        user_2_has_liked: false,
      })
    );
    nextUser();
  }

  function nextUser() {
    const nextIndex = users.length - 2 === currentIndex ? 0 : currentIndex + 1;
    setCurrentIndex(nextIndex);
  }

  function handleLikePress() {
    swipesRef.current.openLeft();
  }
  function handlePassPress() {
    swipesRef.current.openRight();
  }

  return (
    <View style={styles.container}>
      <TopBar />
      <View style={styles.swipes}>
        {users.length > 1 &&
          users.map(
            (u, i) =>
              currentIndex === i && (
                <Swipes
                  key={i}
                  ref={swipesRef}
                  currentIndex={currentIndex}
                  users={users}
                  handleLike={handleLike}
                  handlePass={handlePass}></Swipes>
              )
          )}
      </View>
      <BottomBar
        handleLikePress={handleLikePress}
        handlePassPress={handlePassPress}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: Constants.statusBarHeight,
  },
  swipes: {
    flex: 1,
    padding: 10,
    paddingTop: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 3,
    },
    shadowOpacity: 0.29,
    shadowRadius: 4.65,
    elevation: 7,
  },
});
