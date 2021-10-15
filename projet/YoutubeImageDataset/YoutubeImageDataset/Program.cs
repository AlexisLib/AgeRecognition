using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace YoutubeImageDataset
{
    static class Program
    {
        /// <summary>
        /// Point d'entrée principal de l'application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());

        }
        public static List<bool> GetHash(Bitmap bmpSource)
        {
            List<bool> lResult = new List<bool>();
            //create new image with 16x16 pixel
            Bitmap bmpMin = new Bitmap(bmpSource, new Size(16, 16));
            for (int j = 0; j < bmpMin.Height; j++)
            {
                for (int i = 0; i < bmpMin.Width; i++)
                {
                    //reduce colors to true / false                
                    lResult.Add(bmpMin.GetPixel(i, j).GetBrightness() < 0.5f);
                }
            }
            bmpSource.Dispose();
            bmpMin.Dispose();
            return lResult;
        }

        public static void RemoveDoubles(string dir)
        {
            string[] files = Directory.GetFiles(dir);
            List<List<bool>> HashList = new List<List<bool>>();
            int imageDeleted = 0;
            bool deleted = false;
            foreach (string file in files)
            {
                List<bool> tmpHash = GetHash(new Bitmap(file));
                foreach (var hash in HashList)
                {
                    Application.DoEvents();
                    int equalElements = hash.Zip(tmpHash, (i, j) => i == j).Count(eq => eq);
                    if (equalElements >= 256)
                    {
                        var tmpFile = Path.GetFileName(file);
                        File.Delete(file);
                        imageDeleted++;
                        deleted = true;
                        break;
                    }
                }
                 if (deleted == false)
                    HashList.Add(tmpHash);
                deleted = false;

            }
            Debug.WriteLine(dir + " = " + imageDeleted);
            HashList.Clear();
        }
    }
}
