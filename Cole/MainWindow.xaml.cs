using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Xml.Linq;

namespace Cole {
    /// <summary>
    /// Logique d'interaction pour MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window {
        public MainWindow() {
            InitializeComponent();

            // initialise listbox
            var actorList = XElement.Load("actorList.xml").Elements("Actor").ToList();
            foreach (var actor in actorList) {
                string name = actor.Attribute("Name").Value;
                listBox.Items.Add(name);
            }
        }

        private void searchBox_TextChanged(object sender, TextChangedEventArgs e) {
            // load the actor data and make a list out of it
            var xml = XElement.Load("actorList.xml");
            var actorList = xml.Elements("Actor").ToList();

            // get the typed text, using lower case to avoid issues
            string searchInput = searchBox.Text.ToLowerInvariant();

            // make a list of the search results
            var results = new List<string>();

            // clear the listbox
            listBox.Items.Clear();

            // iterate through the XML to find a match
            // if there's one add it to the results list
            // otherwise remove it
            foreach (var actor in actorList) {
                string actorName = actor.Attribute("Name").Value;
                string actorID = actor.Attribute("ID").Value;
                bool nameOrIdHasInput = (
                    actorName.ToLowerInvariant().Contains(searchInput) ||
                    actorID.ToLowerInvariant().Contains(searchInput)
                );

                if (nameOrIdHasInput) {
                    results.Add(actorName);
                } else {
                    results.Remove(actorName);
                }
            }

            // finally, iterate through the results to add them to the listbox on screen
            // ``results.Distinct().ToList()`` removes duplicates
            foreach (var result in results.Distinct().ToList()) {
                listBox.Items.Add(result);
            }
        }
    }
}
