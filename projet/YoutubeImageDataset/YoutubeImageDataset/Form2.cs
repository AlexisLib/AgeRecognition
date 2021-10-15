using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace YoutubeImageDataset
{
    public partial class Form2 : Form
    {
        private bool _selecting;
        private Rectangle _selection;
        private bool isDrawed;

        public Form2()
        {
            InitializeComponent();
        }

        private void pictureBox_MouseUp(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left &&
                _selecting)
            {
                using (var g = Graphics.FromImage(pictureBox.BackgroundImage))
                {
                    Pen pen = Pens.GreenYellow;
                    g.DrawRectangle(pen, _selection);
                    isDrawed = true;
                }
            }
            _selecting = false;
        }

        private void pictureBox_MouseDown(object sender, MouseEventArgs e)
        {
            // Starting point of the selection:
            if (e.Button == MouseButtons.Left)
            {
                //reload image
                if (isDrawed)
                {
                    string sourcePath = Application.OpenForms["Form1"].Controls["SelectedSourceFolder"].Text;
                    string[] files = Directory.GetFiles(sourcePath);
                    pictureBox.BackgroundImage = Image.FromFile(files[0]);
                    isDrawed = false;
                }
                _selecting = true;
                _selection = new Rectangle(new Point(e.X, e.Y), new Size());
            }
        }

        private void pictureBox_Paint(object sender, PaintEventArgs e)
        {
            if (_selecting)
            {
                // Draw a rectangle displaying the current selection
                Pen pen = Pens.GreenYellow;
                e.Graphics.DrawRectangle(pen, _selection);
            }
        }
        private void pictureBox_MouseMove(object sender, MouseEventArgs e)
        {
            // Update the actual size of the selection:
            if (_selecting)
            {
                _selection.Width = e.X - _selection.X;
                _selection.Height = e.Y - _selection.Y;

                // Redraw the picturebox:
                pictureBox.Refresh();
            }
        }
        private void CancelCrop_Click(object sender, EventArgs e)
        {
            isDrawed = false;
            this.Close();
        }

        private void AcceptCropping_Click(object sender, EventArgs e)
        {
            Debug.WriteLine("W" + _selection.Width);
            Debug.WriteLine("H" + _selection.Height);

            AcceptCropping.Enabled = false;
            string sourcePath = Application.OpenForms["Form1"].Controls["SelectedSourceFolder"].Text;
            string destPath = Application.OpenForms["Form1"].Controls["SelectedDestinationFolder"].Text;
            isDrawed = false;
            string[] files = Directory.GetFiles(sourcePath);
            foreach (string file in files)
            {
                Application.DoEvents();
                Bitmap bmp = new Bitmap(file);
                string filename = Path.GetFileName(file);
                Bitmap cropBmp = bmp.Clone(_selection, bmp.PixelFormat);
                cropBmp.Save(destPath + filename);
                cropBmp.Dispose();
                bmp.Dispose();
            }
            AcceptCropping.Enabled = true;
            this.Close();
        }
    }
}
