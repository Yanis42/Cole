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

        // get "position" data
        public Thickness GetMargin(short left, short top, short right, short bottom) {
            var margin = new Thickness();

            margin.Left = left;
            margin.Top = top + 27;
            margin.Right = right;
            margin.Bottom = bottom;

            return margin;
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
                            // if the current child is the type box
                            // clear its item list
                            child.IsEnabled = true;
                            comboBox.Items.Clear();

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

        // initialises the `typeBox` ComboBox
        private void ProcessActorType(XElement actor) {
            var typeList = new List<XElement>();
            try {
                typeList = actor.Element("Type").Elements("Item").ToList();

                foreach (XElement item in typeList) {
                    UI.typeBox.Items.Add(item.Value);
                }
                UI.typeBox.SelectedIndex = 0;
            } catch (System.NullReferenceException) {
                UI.typeBox.IsEnabled = false;
            }
        }

        private void ProcessActorEnum(XElement Enum, short topValue) {
            var enumList = new List<XElement>();
            enumList = Enum.Elements("Item").ToList();

            ComboBox enumBox = (ComboBox)AddComponent(
                ComponentType.comboBox, "enumBox", null, GetMargin(185, topValue, 10, 0)
            );

            Label label = (Label)AddComponent(
                ComponentType.label, "label", Enum.Attribute("Name").Value,
                GetMargin(5, (short)(topValue - 2), 102, 0)
            );

            foreach (XElement item in enumList) {
                enumBox.Items.Add(item.Attribute("Name").Value);
            }
            enumBox.SelectedIndex = 0;
        }

        private void ProcessActorProperty(XElement property, short topValue) {
            TextBox propertyBox = (TextBox)AddComponent(
                ComponentType.textBox, "propertyBox", null, GetMargin(185, topValue, 10, 0)
            );

            Label label = (Label)AddComponent(
                ComponentType.label, "label", property.Attribute("Name").Value,
                GetMargin(5, (short)(topValue - 2), 102, 0)
            );
        }

        private void ProcessActorFlag(XElement flag, short topValue) {
            TextBox flagBox = (TextBox)AddComponent(
                ComponentType.textBox, "flagBox", null, GetMargin(185, topValue, 10, 0)
            );

            Label label = (Label)AddComponent(
                ComponentType.label, "label",
                (flag.Attribute("Type").Value + " Flag"), GetMargin(5, (short)(topValue - 2), 102, 0)
            );
        }

        private void ProcessActorBool(XElement Bool, short topValue) {
            CheckBox flagBox = (CheckBox)AddComponent(
                ComponentType.checkBox, "boolBox", Bool.Attribute("Name").Value,
                GetMargin(10, topValue, 102, 0)
            );
        }

        public void ProcessActor(XElement actor) {
            short topValue = 0;
            ProcessActorType(actor);

            var enumList = actor.Elements("Enum")?.ToList();
            if (enumList != null) {
                foreach (XElement elem in enumList) {
                    topValue += 27;
                    ProcessActorEnum(elem, topValue);
                }
            }

            var propertyList = actor.Elements("Property")?.ToList();
            if (propertyList != null) {
                foreach (XElement elem in propertyList) {
                    topValue += 27;
                    ProcessActorProperty(elem, topValue);
                }
            }

            var flagList = actor.Elements("Flag")?.ToList();
            if (flagList != null) {
                foreach (XElement elem in flagList) {
                    topValue += 27;
                    ProcessActorFlag(elem, topValue);
                }
            }

            var boolList = actor.Elements("Bool")?.ToList();
            if (boolList != null) {
                foreach (XElement elem in boolList) {
                    topValue += 27;
                    ProcessActorBool(elem, topValue);
                }
            }
        }
    }
}
