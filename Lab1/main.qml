import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 480
    height: 640
    color: "lightgray"
    title: qsTr("Encryption App")

    function encryptGronsfeld(text, key) 
    {
        var result = "";
        var keyIndex = 0;

        for (var i = 0; i < text.length; ++i) 
        {
            var curChar = text[i];


            if (!((curChar >= "a" && curChar <= "z"))) 
            {
                result += curChar;
                continue;
            }

            var keyDigit = parseInt(key[keyIndex]); //parseInt = str to int

 
            var encryptedCharCode = (curChar.charCodeAt(0) + keyDigit); // curChar.charCodeAt(0) - char код 1 символа строки curChar


            if (encryptedCharCode > "z".charCodeAt(0)) 
            {
                encryptedCharCode -= 26;  // избегаем выпадения из алфавита
            }

            var encryptedChar = String.fromCharCode(encryptedCharCode);
            result += encryptedChar;

            keyIndex = (keyIndex + 1) % key.length; // переход к след. цифре
        }

        return result;
    }

    ColumnLayout 
    {
        anchors.fill: parent

        TextField 
        {
            id: inputField
            placeholderText: qsTr("Enter text")
            font.pointSize: 16
            Layout.preferredWidth: parent.width / 2
            Layout.fillWidth: true
        }

        TextField 
        {
            id: keyField
            placeholderText: qsTr("Enter key")
            font.pointSize: 16
            Layout.preferredWidth: parent.width / 2
            Layout.fillWidth: true
        }

        Button 
        {
            text: "Encrypt"
            font.pointSize: 16
            onClicked: { encryptedText.text = encryptGronsfeld(inputField.text, keyField.text); }
        }

        Rectangle 
        {
            width: encryptedText.width + 10  
            height: encryptedText.height + 10 
            color: "#6A7B8B" 
            border.color: "#7F7B8B"  
            border.width: 3  

            Text 
            {
                id: encryptedText
                text: "Encrypted Result"
                font.pointSize: 16
                color: "white" 
                anchors.centerIn: parent 
            }
        }


        Button 
        {
            text: "Exit"
            font.pointSize: 16
            onClicked: Qt.quit()
        }
    }
}
