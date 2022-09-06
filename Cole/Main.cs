using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Xml.Linq;

namespace Cole {
    public class Main {
        MainWindow UI = Application.Current.Windows[0] as MainWindow;
        XElement actorFile = XElement.Load("actorList.xml");

        public void Init() {
            // initialise listbox
            var actorList = actorFile.Elements("Actor").ToList();

            foreach (var actor in actorList) {
                string name = actor.Attribute("Name").Value;
                UI.listBox.Items.Add(name);
            }
        }

        // logic for the search system
        public void SearchUpdate() {
            // load the actor data and make a list out of it
            var actorList = actorFile.Elements("Actor").ToList();

            // get the typed text, using lower case to avoid issues
            string searchInput = UI.searchBox.Text.ToLowerInvariant();

            // make a list of the search results
            var results = new List<string>();

            // clear the listbox
            UI.listBox.Items.Clear();

            // iterate through the XML to find a match
            // if there's one add it to the results list
            // otherwise remove it
            foreach (var actor in actorList) {
                string actorName = actor.Attribute("Name").Value,
                actorID = actor.Attribute("ID").Value, actorKey = actor.Attribute("Key").Value;

                bool nameOrIdHasInput = (
                    actorName.ToLowerInvariant().Contains(searchInput) ||
                    actorID.ToLowerInvariant().Contains(searchInput) ||
                    actorKey.ToLowerInvariant().Contains(searchInput)
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
                UI.listBox.Items.Add(result);
            }
        }

        // logic for selecting an actor from the list
        public void ItemUpdate() {
            var actorList = actorFile.Elements("Actor").ToList();

            // get the selection's value, in this case the actor's name
            string selectedActor = (string)UI.listBox.SelectedValue;

            // iterate through the list to find the correct actor
            foreach (var actor in actorList) {
                string actorName = actor.Attribute("Name").Value;

                // once we found it, draw the parameters
                if (actorName == selectedActor) {
                    Console.WriteLine("Selected Actor: {0}", actor.Attribute("ID").Value);
                }
            }
        }
    }
}
