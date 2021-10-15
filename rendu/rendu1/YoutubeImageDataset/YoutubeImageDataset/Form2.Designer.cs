namespace YoutubeImageDataset
{
    partial class Form2
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBox = new System.Windows.Forms.PictureBox();
            this.AcceptCropping = new System.Windows.Forms.Button();
            this.CancelCrop = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBox
            // 
            this.pictureBox.Location = new System.Drawing.Point(63, 66);
            this.pictureBox.Name = "pictureBox";
            this.pictureBox.Size = new System.Drawing.Size(977, 546);
            this.pictureBox.TabIndex = 0;
            this.pictureBox.TabStop = false;
            this.pictureBox.Paint += new System.Windows.Forms.PaintEventHandler(this.pictureBox_Paint);
            this.pictureBox.MouseDown += new System.Windows.Forms.MouseEventHandler(this.pictureBox_MouseDown);
            this.pictureBox.MouseMove += new System.Windows.Forms.MouseEventHandler(this.pictureBox_MouseMove);
            this.pictureBox.MouseUp += new System.Windows.Forms.MouseEventHandler(this.pictureBox_MouseUp);
            // 
            // AcceptCropping
            // 
            this.AcceptCropping.Location = new System.Drawing.Point(1892, 1459);
            this.AcceptCropping.Name = "AcceptCropping";
            this.AcceptCropping.Size = new System.Drawing.Size(747, 96);
            this.AcceptCropping.TabIndex = 1;
            this.AcceptCropping.Text = "Accept Cropping";
            this.AcceptCropping.UseVisualStyleBackColor = true;
            this.AcceptCropping.Click += new System.EventHandler(this.AcceptCropping_Click);
            // 
            // CancelCrop
            // 
            this.CancelCrop.Location = new System.Drawing.Point(63, 1459);
            this.CancelCrop.Name = "CancelCrop";
            this.CancelCrop.Size = new System.Drawing.Size(747, 96);
            this.CancelCrop.TabIndex = 2;
            this.CancelCrop.Text = "Cancel";
            this.CancelCrop.UseVisualStyleBackColor = true;
            this.CancelCrop.Click += new System.EventHandler(this.CancelCrop_Click);
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(12F, 25F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.AutoSize = true;
            this.ClientSize = new System.Drawing.Size(2704, 1665);
            this.Controls.Add(this.CancelCrop);
            this.Controls.Add(this.AcceptCropping);
            this.Controls.Add(this.pictureBox);
            this.Name = "Form2";
            this.Text = "Form2";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.PictureBox pictureBox;
        private System.Windows.Forms.Button AcceptCropping;
        private System.Windows.Forms.Button CancelCrop;
    }
}