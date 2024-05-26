import { Dimensions, StyleSheet } from 'react-native';
import Theme from './Theme';

const { width, height } = Dimensions.get('window');

const GlobalStyle = StyleSheet.create({
    Container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    Center: {
        alignItems: 'center',
        justifyContent: 'center',
    },
    HelpText: {
        marginBottom: 12,
        marginTop: -16,
        fontSize: 16,
        fontFamily: Theme.Bold,
        textAlign: 'center',
    },
    BackGround: {
        width: '100%',
        height: '100%',
        backgroundColor: 'white',
    },
    ModalContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 22,
        backgroundColor: 'rgba(52, 52, 52, 0.8)',
    },
    ModalView: {
        margin: 20,
        backgroundColor: 'white',
        borderRadius: 20,
        padding: 35,
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: {
            width: 0,
            height: 2,
        },
    },
    ModalTitle: {
        color: Theme.PrimaryColor,
        fontSize: 20,
        fontFamily: Theme.Bold,
        marginBottom: 20,
    },
    DialogButton: {
        color: Theme.PrimaryColor,
        fontSize: 16,
    },
    HeaderButton: {
        width: width / 4,
        height: 40,
        padding: 8,
        borderRadius: 16,
        backgroundColor: Theme.PrimaryColor,
    },
    HeaderButtonText: {
        color: 'white',
        fontFamily: Theme.Bold,
    },
});

export default GlobalStyle;
