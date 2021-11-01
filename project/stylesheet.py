stylesheet = '''
QFrame#frame {
    border-image: url(:bg) 0 0 0 0 stretch stretch;
}

QPushButton#instance-button {
    background-color: rgba(0, 0, 0, .5);
    border: 1px solid rgba(0, 0, 0, .1);
    color: white;
    padding: 15px 15px;
    border-radius: 4px;
    text-align: left;
}

QPushButton#instance-button:hover {
    background-color: rgba(0, 0, 0, .7);
}

QScrollArea#scroll {
    background-color: transparent; border: none;
}

QWidget#container {
    background-color: transparent;
}
'''
