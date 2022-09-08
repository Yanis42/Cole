using System.Windows;
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
        }

        // get "position" data
        public Thickness GetMargin(short left, short top, short right, short bottom) {
            var margin = new Thickness();

            margin.Left = left;
            margin.Top = top;
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
        public void AddComponent(ComponentType type, string name, string label, Thickness margin) {
            switch (type) {
                case ComponentType.comboBox:
                    var comboBox = new ComboBox();
                    UI.paramGrid.Children.Add(comboBox);
                    comboBox.Name = name;
                    comboBox.Margin = margin;
                    comboBox.VerticalAlignment = VerticalAlignment.Top;
                    break;

                case ComponentType.checkBox:
                    var checkBox = new CheckBox();
                    UI.paramGrid.Children.Add(checkBox);
                    checkBox.Name = name;
                    checkBox.Margin = margin;
                    checkBox.VerticalAlignment = VerticalAlignment.Top;
                    checkBox.Content = (label != null) ? label : "Error";
                    break;

                case ComponentType.textBox:
                    var textBox = new TextBox();
                    UI.paramGrid.Children.Add(textBox);
                    textBox.Name = name;
                    textBox.Margin = margin;
                    textBox.VerticalAlignment = VerticalAlignment.Top;
                    textBox.TextWrapping = TextWrapping.Wrap;
                    textBox.MaxLines = 1;
                    textBox.Height = 20;
                    break;

                default:
                    MessageBox.Show(("Component Type Error!"), "Cole");
                    break;
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
    }
}
