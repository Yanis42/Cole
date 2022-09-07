using System.Windows;
using System.Windows.Controls;
#nullable disable

namespace Cole {
    public partial class MainWindow : Window {
        // prevent stack overflow exceptions
        Main main = null;

        // initialisation of the app
        public MainWindow() {
            InitializeComponent();

            // now that components are initialised,
            // we can call our main class and initialise it
            main = new Main();
            main.Init();
        }

        // update the result list on text update
        private void searchBox_TextChanged(object sender, TextChangedEventArgs e) {
            main.SearchUpdate();
        }

        // show parameters on selection update
        private void listBox_SelectionChanged(object sender, SelectionChangedEventArgs e) {
            main.ItemUpdate();
        }
    }
}
