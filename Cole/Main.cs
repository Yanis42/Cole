using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Xml.Linq;
using System.IO;
#nullable disable

namespace Cole {
    public class Main {
        ComponentManager manager = null;
        MainWindow UI = Application.Current.Windows[0] as MainWindow;
        XElement actorFile = null, objectFile = null;

        // tries to open the file set in the parameters
        // if it fails, prompts a dialog to get it
        private XElement GetXmlData(string path) {
            XElement file = null;
            try {
                file = XElement.Load(path);
            } catch (FileNotFoundException) {
                var openFile = new System.Windows.Forms.OpenFileDialog();
                MessageBox.Show(("File ``" + path + "`` not found!"), "Cole");

                openFile.Filter = "XML Files (*.xml)|*.xml";
                openFile.Title = "Select the XML file";
                if (openFile.ShowDialog() == System.Windows.Forms.DialogResult.OK) {
                    file = XElement.Load(openFile.FileName);
                }
            }
            return file;
        }

        // initialise components' content
        public void Init() {
            // initialise the component manager
            manager = new ComponentManager();

            // get the data
            actorFile = GetXmlData("actorList.xml");
            objectFile = GetXmlData("objectList.xml");

            // make lists out of them
            var actorList = actorFile.Elements("Actor").ToList();
            var objectList = objectFile.Elements("Object").ToList();

            // create empty lists for combo box
            var categories = new List<string>();
            categories.Add("All");

            // then fill it
            foreach (var actor in actorList) {
                string actorName = actor.Attribute("Name").Value;
                string actorCategory = actor.Attribute("Category").Value.Replace("ACTORCAT_", "");

                UI.actorListBox.Items.Add(actorName);
                categories.Add(char.ToUpper(actorCategory[0]) + actorCategory.Substring(1));
            }
            foreach (var category in categories.Distinct().ToList()) {
                UI.categoryBox.Items.Add(category);
            }
        }

        // logic for the search system
        public void ActorSearchUpdate() {
            // load the actor data and make a list out of it
            var actorList = actorFile.Elements("Actor").ToList();

            // get the typed text, using lower case to avoid issues
            string searchInput = UI.actorSearchBox.Text.ToLowerInvariant();

            // get the category
            string categoryInput = "ACTORCAT_" + (string)UI.categoryBox.SelectedValue;

            // make a list of the search results
            var results = new List<string>();

            // clear the actorListBox
            UI.actorListBox.Items.Clear();

            // iterate through the XML to find a match
            // if there's one add it to the results list
            // otherwise remove it
            foreach (var actor in actorList) {
                string actorName = actor.Attribute("Name").Value, actorID = actor.Attribute("ID").Value,
                actorKey = actor.Attribute("Key").Value, actorCategory = actor.Attribute("Category").Value;

                bool nameFilter = (
                    actorName.ToLowerInvariant().Contains(searchInput) ||
                    actorID.ToLowerInvariant().Contains(searchInput) ||
                    actorKey.ToLowerInvariant().Contains(searchInput)
                );

                bool categoryFilter = (
                    actorCategory == categoryInput.ToUpper() || categoryInput.ToUpper() == "ACTORCAT_ALL"
                );

                if (categoryFilter) {
                    results.Add(actorName);

                    if (nameFilter) {
                        results.Add(actorName);
                    } else {
                        results.Remove(actorName);
                    }
                } else {
                    results.Remove(actorName);
                }
            }

            // finally, iterate through the results to add them to the actorListBox on screen
            // ``results.Distinct().ToList()`` removes duplicates
            results = results.Distinct().ToList();
            foreach (var result in results) {
                UI.actorListBox.Items.Add(result);
            }

            UI.foundLabel.Content = "Found: " + results.Count.ToString();
        }

        // logic for selecting an actor from the list
        public void ItemUpdate() {
            var actorList = actorFile.Elements("Actor").ToList();

            // get the selection's value, in this case the actor's name
            string selectedActor = (string)UI.actorListBox.SelectedValue;

            // iterate through the list to find the correct actor
            foreach (var actor in actorList) {
                string actorName = actor.Attribute("Name").Value;

                // once we found it, draw the parameters
                if (actorName == selectedActor) {
                    // start by resetting the grid
                    manager.ResetParamGrid();

                    // debug print
                    Console.WriteLine("Selected Actor: {0}", actor.Attribute("ID").Value);

                    // get out of the loop as we found the actor
                    break;
                }
            }
        }
    }
}
