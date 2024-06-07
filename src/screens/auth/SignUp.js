import { LinearGradient } from 'expo-linear-gradient';
import React, { useState } from 'react';
import { Alert, ScrollView } from 'react-native';
import AuthFooter from '../../components/auth/AuthFooter';
import AuthForm from '../../components/auth/AuthForm';
import AuthHeader from '../../components/auth/AuthHeader';
import DismissKeyboard from '../../components/common/DismissKeyboard';
import APIs, { endPoints } from '../../configs/APIs';
import { statusCode } from '../../configs/Constants';
import { useGlobalContext } from '../../store/contexts/GlobalContext';
import GlobalStyle from '../../styles/Style';
import Theme from '../../styles/Theme';
import { signUpFields } from '../../utils/Fields';

const SignUp = ({ navigation }) => {
   const { loading, setLoading } = useGlobalContext();

   const [account, setAccount] = useState({});
   const [errorMessage, setErrorMessage] = useState('');
   const [errorVisible, setErrorVisible] = useState(false);

   const handleSignUp = async () => {
      for (let field of signUpFields) {
         if (!account[field.name]) {
            setErrorVisible(true);
            setErrorMessage(field.errorMessage);
            return;
         }
      }

      if (account['password'] !== account['confirm']) {
         setErrorVisible(true);
         setErrorMessage('Mật khẩu không khớp');
         return;
      }

      let form = new FormData();
      for (let key in account)
         if (key !== 'confirm') form.append(key, key !== 'password' ? account[key].trim() : account[key]);

      setLoading(true);
      setErrorVisible(false);
      try {
         let res = await APIs.post(endPoints['student-register'], form, {
            headers: {
               'Content-Type': 'multipart/form-data',
            },
         });

         if (res.status === statusCode.HTTP_201_CREATED) {
            Alert.alert(
               'Đăng ký thành công',
               'Chuyển sang đăng nhập?',
               [
                  { text: 'Đăng nhập', onPress: () => navigation.navigate('SignIn') },
                  { text: 'Hủy', style: 'cancel' },
               ],
               { cancelable: true },
            );
         }
      } catch (error) {
         if (error.response && error.response.status === statusCode.HTTP_400_BAD_REQUEST) {
            setErrorVisible(true);
            setErrorMessage(error.response.data.detail);
         } else console.error(error);
      } finally {
         setLoading(false);
      }
   };

   return (
      <ScrollView style={GlobalStyle.BackGround}>
         <DismissKeyboard>
            <LinearGradient colors={Theme.LinearColors2}>
               <AuthHeader title="Đăng ký" content="Đăng ký để sử dụng hệ thống điểm rèn luyện sinh viên" />
               <AuthForm
                  fields={signUpFields}
                  account={account}
                  setAccount={setAccount}
                  errorVisible={errorVisible}
                  errorMessage={errorMessage}
                  loading={loading}
                  onPressFunc={handleSignUp}
                  buttonText="Đăng ký"
               />
               <AuthFooter navigation={navigation} content="Đã có tài khoản?" screen="SignIn" linkText="Đăng nhập" />
            </LinearGradient>
         </DismissKeyboard>
      </ScrollView>
   );
};

export default SignUp;