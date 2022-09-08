using System.Linq;
using System.Windows;
using System.Xml.Linq;
using System.Windows.Controls;
using System.Collections.Generic;
#nullable disable

namespace Cole
{
    public class ComponentManager {
        MainWindow UI = Application.Current.Windows[0] as MainWindow;

        // type of the component to add
        public enum ComponentType {
            /* 0 */ comboBox,
            /* 1 */ checkBox,
            /* 2 */ textBox,
            /* 3 */ label,
        }

        /***********************
         *  Get/Set Functions  *
         ***********************/

        // returns the list of element inside ``<List>`` nodes in the XML
        private List<XElement> GetList(XElement actorFile, string listName) {
            var list = actorFile.Elements("List").ToList();
            List<XElement> itemList = null;

            foreach (XElement elem in list) {
                if (elem.Attribute("Name").Value == listName) {
                    itemList = elem.Elements("Item").ToList();
                    break;
                }
            }
            return itemList;
        }

        // get "position" data
        public Thickness GetMargin(short left, short top, short right, short bottom) {
            var margin = new Thickness();

            margin.Left = left;
            margin.Top = top + 27; // account for the type combo box
            margin.Right = right;
            margin.Bottom = bottom;

            return margin;
        }

        /***********************
         * Component Functions *
         ***********************/

        // removes every components added for parameters
        public void ResetParamGrid() {
            // list of components to remove
            var toRemove = new List<UIElement>();

            // loop through every childrens of the param grid
            foreach (UIElement child in UI.paramGrid.Children) {
                var childType = child.GetType();

                // if the current element isn't a GroupBox
                if ((childType != typeof(GroupBox))) {
                    // or if it's a ComboBox but the name isn't "typeBox"
                    if (childType == typeof(ComboBox)) {
                        ComboBox comboBox = (ComboBox)child;
                        if (comboBox.Name == "typeBox") {
                            // `continue` stops the current iteration
                            // and go to the next one
                            continue;
                        }
                    }

                    // add the current element to the list
                    toRemove.Add(child);
                }
            }

            // finally, remove every elements of the list from the grid
            foreach (UIElement elem in toRemove) {
                UI.paramGrid.Children.Remove(elem);
            }
        }

        /** Adds a component.
          *
          * Parameters:
          * ``ComponentType type``: the type of component to add
          * ``string name``: the name of the component, like an ID
          * ``string label``: the description of the component
          * ``Thickness margin``: position data
          */
        public object AddComponent(ComponentType type, string name, string label, Thickness margin) {
            switch (type) {
                case ComponentType.comboBox:
                    var comboBox = new ComboBox();
                    UI.paramGrid.Children.Add(comboBox);
                    comboBox.Name = name;
                    comboBox.Margin = margin;
                    comboBox.VerticalAlignment = VerticalAlignment.Top;
                    return comboBox;
                case ComponentType.checkBox:
                    var checkBox = new CheckBox();
                    UI.paramGrid.Children.Add(checkBox);
                    checkBox.Name = name;
                    checkBox.Margin = margin;
                    checkBox.VerticalAlignment = VerticalAlignment.Top;
                    checkBox.Content = (label != null) ? label : "Error";
                    return checkBox;
                case ComponentType.textBox:
                    var textBox = new TextBox();
                    UI.paramGrid.Children.Add(textBox);
                    textBox.Name = name;
                    textBox.Margin = margin;
                    textBox.VerticalAlignment = VerticalAlignment.Top;
                    textBox.TextWrapping = TextWrapping.Wrap;
                    textBox.MaxLines = 1;
                    textBox.Height = 20;
                    return textBox;
                case ComponentType.label:
                    var uiLabel = new Label();
                    UI.paramGrid.Children.Add(uiLabel);
                    uiLabel.Content = (label != null) ? label : "Error";
                    uiLabel.Margin = margin;
                    uiLabel.VerticalAlignment = VerticalAlignment.Top;
                    return uiLabel;
                default:
                    MessageBox.Show(("Component Type Error!"), "Cole");
                    return null;
            }
        }

        // add a new label to the UI
        private void AddLabel(string displayName, short topValue) {
            Label label = (Label)AddComponent(
                ComponentType.label, "label", displayName, GetMargin(5, topValue, 102, 0)
            );
        }

        // add a combo box on the ui
        private void AddComboBox(XElement elem, short topValue, List<XElement> itemList, string labelName) {
            // the item list needs to be defined
            if (itemList != null) {
                AddLabel(labelName, (short)(topValue - 2));
                ComboBox comboBox = (ComboBox)AddComponent(
                    ComponentType.comboBox, "enumBox", null, GetMargin(185, topValue, 10, 0)
                );

                // populate the combo box item list
                foreach (XElement item in itemList) {
                    comboBox.Items.Add(item.Attribute("Name").Value);
                }
                // select first element by default
                comboBox.SelectedIndex = 0;
            }
        }

        // add a textbox on the ui
        private void AddTextBox(XElement elem, short topValue, string name) {
            string displayName = "Name";
            TextBox textBox = (TextBox)AddComponent(
                ComponentType.textBox, name, null, GetMargin(185, topValue, 10, 0)
            );

            // special case for flags
            displayName = (name == "flagBox") ? (elem.Attribute("Type").Value + " Flag")
                        : elem.Attribute("Name").Value;

            AddLabel(displayName, (short)(topValue - 2));
        }

        // add a checkbox on the ui
        private void AddCheckBox(XElement elem, short topValue) {
            CheckBox flagBox = (CheckBox)AddComponent(
                ComponentType.checkBox, "boolBox", elem.Attribute("Name").Value,
                GetMargin(10, topValue, 102, 0)
            );
        }

        /***********************
         *   Actor Processor   *
         ***********************/

        // initialises the `typeBox` ComboBox
        private void InitActorType(XElement actor) {
            // enable the type box and clear its item list
            UI.typeBox.IsEnabled = true;
            UI.typeBox.Items.Clear();

            // get every items from the type sub-element
            // disable the combo box if the list is null
            var typeList = new List<XElement>();
            try {
                typeList = actor.Element("Type").Elements("Item").ToList();

                foreach (XElement item in typeList) {
                    UI.typeBox.Items.Add(item.Value);
                }
                // select the first element by default
                UI.typeBox.SelectedIndex = 0;
            } catch (System.NullReferenceException) {
                UI.typeBox.IsEnabled = false;
            }
        }

        // main logic of the actor processor
        private short ProcessActor(XElement actorFile, XElement actor, string tag, short topValue) {
            var list = actor.Elements(tag)?.ToList();
            var itemList = new List<XElement>();

            // if the list is not null it means we need to draw
            // a new element on the UI
            if (list != null) {
                foreach (XElement elem in list) {
                    topValue += 27;

                    // do different actions depending on what we need to draw
                    switch (tag) {
                        case "Enum":
                            AddComboBox(
                                elem,
                                topValue,
                                elem.Elements("Item").ToList(),
                                elem.Attribute("Name").Value
                            );
                            break;
                        case "Property":
                            AddTextBox(elem, topValue, "propertyBox");
                            break;
                        case "Flag":
                            AddTextBox(elem, topValue, "flagBox");
                            break;
                        case "Bool":
                            AddCheckBox(elem, topValue);
                            break;
                        case "Message":
                            AddComboBox(
                                elem,
                                (short)(topValue - 2),
                                GetList(actorFile, "Elf_Msg Message ID"),
                                "Message ID"
                            );
                            break;
                        case "ChestContent":
                            AddComboBox(
                                elem,
                                (short)(topValue - 2),
                                GetList(actorFile, "Chest Content"),
                                "Chest Content"
                            );
                            break;
                        case "Collectible":
                            AddComboBox(
                                elem,
                                (short)(topValue - 2),
                                GetList(actorFile, "Collectibles"),
                                "Collectibles"
                            );
                            break;
                        default:
                            break;
                    }
                }
            }
            return topValue;
        }

        // called by Main, initialises and run the processor
        public void InitActorProcess(XElement actorFile, XElement actor) {
            // ``topValue`` defines the Y-Pos of an element
            // it's incremented by 27 before each use
            short topValue = 0;
            string[] tagList = new string[] {
                "Enum", "Property", "Flag", "Bool", "Message", "ChestContent", "Collectible"
            };

            // init the type combo box
            InitActorType(actor);

            // run the processor for each tag in the list
            foreach (string tag in tagList) {
                topValue = ProcessActor(actorFile, actor, tag, topValue);
            }
        }
    }
}
